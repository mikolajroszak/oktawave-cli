import os

import click

from oktawave.api import TemplateOrigin
from oktawave.commands.context import pass_context, positional_option, OktawaveCliGroup, NamedItemParam
from oktawave.commands.util import print_templates


class TemplateParam(NamedItemParam):
    name = 'Template name/id'
    label = 'Template'

    @classmethod
    def list_items(cls, api):
        for item in api.Template_ListAll():
            yield item['id'], item['name']

def template_id_param(*args, **kwargs):
    kwargs.setdefault('help', 'Template ID (as returned by Template List)')
    kwargs.setdefault('type', TemplateParam())
    return positional_option(*args, **kwargs)


@click.command(cls=OktawaveCliGroup, name='Template')
def Template():
    """Get information about available OCI templates"""
    pass


@Template.command()
@positional_option('category', type=click.Choice(TemplateOrigin.names), required=False, help='Template category.')
@pass_context
def Template_List(ctx, category):
    """List available template categories"""
    templates = []
    if category:
        templates = ctx.api.Template_List(category)
    else:
        templates = ctx.api.Template_ListAll()
    print_templates(ctx, templates) 

@Template.command()
@template_id_param('template_id')
@pass_context
def Template_Show(ctx, template_id):
    """Shows more detailed info about a particular template"""
    ti = ctx.api.Template_Show(template_id)

    def _hdd_label(hdd):
        if hdd['is_primary']:
            return '%(name)s (%(capacity_gb)d GB, Primary)' % hdd
        else:
            return '%(name)s (%(capacity_gb)d GB)' % hdd

    tab = [['Key', 'Value']]
    tab.extend([
        ['Template ID', ti['template_id']],
        ['VM class', '%s (class ID: %s)' % (ti['vm_class_name'], ti['vm_class_id'])],
        ['Name', ti['label']],
        ['Template name', ti['template_name']],
        ['System category', ti['system_category_name']],
        ['Template category', ti['template_category']],
        ['Software', ', '.join(str(s) for s in ti['software'])],
        ['Ethernet controllers', ti['eth_count']],
        ['Connection', ti['connection_type']],
        ['Disk drives', ', '.join(_hdd_label(hdd) for hdd in ti['disks'])],
        ['Description', ti['description']],
    ])
    ctx.p.print_table(tab)

