from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['./templates'], output_encoding='utf-8', encoding_errors='replace')

def render(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)
