# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Use hashicorp/bionic64 as Vagrant development environment box.
  config.vm.box = "hashicorp/bionic64"

  # Create a forwarded port mapping (although this does not seem to work with 
  # hyperv provider. 
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Create a public network 
  config.vm.network "public_network"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. 
  #
  # View the documentation for the provider you are using for more
  # information on available options.
  config.vm.provider "hyperv" do |h|
    h.enable_virtualization_extensions = true
    h.linked_clone = true
  end  

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y \
      build-essential \
      libssl-dev \
      zlib1g-dev \
      libbz2-dev \
      libreadline-dev \
      libsqlite3-dev \
      wget \
      curl \
      llvm \
      libncurses5-dev \
      libncursesw5-dev \
      xz-utils \
      tk-dev \
      libffi-dev \
      liblzma-dev \
      python-openssl \
      git
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    echo 'export CFLAGS="-O2"' >> ~/.bash_profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
    source ~/.bash_profile
    pyenv install 3.8.5
    pyenv global 3.8.5
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  # Use the global trigger for "after up" to start the flask application
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    # Install dependencies and launch
    source ~/.bash_profile
    cd /vagrant
    poetry install
    nohup poetry run flask run --host=0.0.0.0 > todoapp.log 2>&1 &
    "}
  end
end