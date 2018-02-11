# Ansible Jenkins View module

It is a module that manages view of jenkins with ansible.

```
- hosts: jenkins_host
  tasks:
    - set_fact:
        list_view_example:
          - name: example_view
            list_job:
              - exmpla_job_a
              - exmpla_job_b
              - exmpla_job_c
              - exmpla_job_d
        list_view_regex_example:
          - name: example_regexp_view
            list_job:
              - exmpla_job_a
            ptn_regex: "exmpla_regex_job.*"

    - name: "Create ordinary view"
      jenkins_view:
        name: "{{ item.name }}"
        list_job: "{{ item.list_job | join(',') }}"
      with_items:
        - "{{ list_view_example }}"

    - name: "Create a job with regular expressions"
      jenkins_view:
        name: "{{ item.name }}"
        list_job: "{{ item.list_job | join(',') }}"
        regex: "{{ item.ptn_regex }}"
      with_items:
        - "{{ list_view_regex_example }}"
```
