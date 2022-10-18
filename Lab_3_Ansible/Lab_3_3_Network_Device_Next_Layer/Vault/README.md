###### Vault password - ansible

* ansible-vault encrypt group_vars/all host_vars/localhost    -    шифруем переменные
* ansible-vault edit group_vars/all    -    редактируем переменные (vim)
* ansible-playbook -i hosts ex_template_cisco_nxos.yml --vault-pass-file .vault_password.txt    -    запуск сценария с паролем в файле
* asible-playbook -i hosts ex_template_cisco_nxos.yml --ask-vault-pass    -    запуск сценария с вводом пароля в CLI
