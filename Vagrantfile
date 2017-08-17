# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "auth.dev.bookmarknovels.com"
  config.vm.network :private_network, ip: "192.168.42.42"

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.include_offline = true

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    # Shared Bookmark Script
    wget -O - --quiet https://raw.githubusercontent.com/Bookmark-Novels/Resources/master/Tools/Scripts/vagrant_bootstrap.sh | sh

    # MySQL
    apt-get install -y libmysqlclient-dev libffi-dev

    # NodeJS
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
    export NVM_DIR="~vagrant/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

    nvm install 6.9.4
    nvm use 6.9.4

    ln -s "$(which nodejs)" /usr/local/bin/node

    # Frontend Dependencies
    apt-get install npm -y
    cd /vagrant && npm install

    npm install -g grunt

    # Ruby - SASS
    apt-get install -y software-properties-common
    apt-add-repository -y ppa:rael-gc/rvm
    apt-get update
    apt-get install -y rvm

    source /etc/profile.d/rvm.sh

    rvm install 2.4.1
    rvm use 2.4.1

    gem install sass

    # Python Dependencies
    pip3 install -r /vagrant/requirements.txt

    cd ~

    # NGINX
    apt-get install -y nginx;
    ln -s /vagrant/conf/nginx /etc/nginx/sites-enabled/gatekeeper;
    nginx -s reload;

    # Redis
    wget http://download.redis.io/releases/redis-4.0.1.tar.gz
    tar -xvf redis-4.0.1.tar.gz
    cd redis-4.0.1 && make install

    echo "redis-server &;" >> ~vagrant/.zshrc
  SHELL
end
