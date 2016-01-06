# config valid only for current version of Capistrano
lock '3.4.0'

set :application, 'HackTester'
set :repo_url, 'git@github.com:HackBulgaria/HackTester.git'

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, '/hack/HackTester'

# Default value for :scm is :git
# set :scm, :git

# Default value for :format is :pretty
# set :format, :pretty

# Default value for :log_level is :debug
# set :log_level, :debug

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# set :linked_files, fetch(:linked_files, []).push('config/database.yml', 'config/secrets.yml')
set :linked_files, fetch(:linked_files, []).push('HackTester/local_settings.py')

# Default value for linked_dirs is []
set :linked_dirs, fetch(:linked_dirs, []).push('static', 'media')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
# set :keep_releases, 5

namespace :deploy do
  task :pip_install do
    on roles(:all) do |h|
      execute "/hack/HackTester/shared/virtualenv/bin/pip install -r /hack/HackTester/current/requirements.txt"
    end
  end

  task :run_migrations do
    on roles(:all) do |h|
      execute "/hack/HackTester/shared/virtualenv/bin/python3 /hack/HackTester/current/manage.py migrate --noinput"
    end
  end

  task :run_collect_static do
    on roles(:all) do |h|
      execute "/hack/HackTester/shared/virtualenv/bin/python3 /hack/HackTester/current/manage.py collectstatic --noinput"
    end
  end

  task :restart do
    on roles(:all) do |h|
      execute "sudo restart HackTester"
    end
  end

  after :published, :pip_install
  after :pip_install, :run_migrations
  after :run_migrations, :run_collect_static
  after :run_migrations, :restart
end