#!/usr/bin/env python

from ansible.module_utils.basic import *
import jenkins
import re

template_config = """        <listView>
            <description>{}</description>
            <jobNames>
{}
            </jobNames>
{}
        </listView>"""

fmt_job = "                <string>{}</string>"
fmt_regex = "<includeRegex>{}</includeRegex>"

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            list_job=dict(required=False),
            regex=dict(required=False),
            description=dict(required=False),
            url=dict(required=False),
        )
    )

    args = module.params

    name_view = args.get('name')
    description = args.get('description') or name_view
    list_job = args.get('list_job').split(',') if args.get('list_job') else []
    ptn_regex = args.get('regex') or ''
    
    xml_job_list = "\n".join(map(lambda x: fmt_job.format(x), list_job))
    xml_regex = fmt_regex.format(ptn_regex)
    xml_config = template_config.format(description, xml_job_list, xml_regex)

    str_url = args.get('url') or 'http://localhost:8080'
    serv_jenkins = jenkins.Jenkins(url)

    if serv_jenkins.view_exists(name_view):
        is_modify = False
        
        list_now_job = []
        for map_job in serv_jenkins.get_jobs(view_name=name_view):
            name_job = map_job['url'].split('/')[-2:-1].pop()
            if 0 != len(ptn_regex) and re.search(ptn_regex, name_job):
                continue
            list_now_job.append(name_job)

        list_checked_job = []
        for name_job in list_job:
            if 0 != len(ptn_regex) and re.search(ptn_regex, name_job):
                continue
            list_checked_job.append(name_job)

        if -1 == serv_jenkins.get_view_config(name_view).find(xml_regex):
            is_modify = True
            
        if set(list_checked_job) != set(list_now_job):
            is_modify = True

        if is_modify:
            serv_jenkins.reconfig_view(name_view, xml_config)
            module.exit_json(message='{} view was modified.upload.'.format(name_view), changed=True)
        else:
            module.exit_json(message='{} view was not modified.'.format(name_view), changed=False)            
    else:
        serv_jenkins.create_view(name_view, xml_config)
        module.exit_json(message='{} view was created.'.format(name_view), changed=True)

if __name__ == '__main__':
    main()
