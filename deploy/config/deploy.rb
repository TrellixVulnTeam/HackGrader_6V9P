# config valid only for current version of Capistrano
lock '3.7.0'

set :application, 'HackTester'
set :repo_url, 'git@github.com:HackBulgaria/HackTester.git'

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, '/hack/hacktester'

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
# set :linked_files, fetch(:linked_files, []).push('source/HackTester/local_settings.py')

# Default value for linked_dirs is []
set :linked_dirs, fetch(:linked_dirs, []).push('static', 'media')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
# set :keep_releases, 5

namespace :deploy do
  task :pip_install do
    on roles(:all) do |h|
      execute "#{fetch :deploy_to}/shared/virtualenv/bin/pip install -r #{fetch :deploy_to}/current/requirements/local.txt"
      execute "#{fetch :deploy_to}/shared/virtualenv/bin/pip install -r #{fetch :deploy_to}/current/requirements/production.txt"
    end
  end

  task :run_migrations do
    on roles(:all) do |h|
      execute "#{fetch :deploy_to}/shared/virtualenv/bin/python3 #{fetch :deploy_to}/current/manage.py migrate --noinput"
    end
  end

  task :run_collect_static do
    on roles(:all) do |h|
      execute "#{fetch :deploy_to}/shared/virtualenv/bin/python3 #{fetch :deploy_to}/current/manage.py collectstatic --noinput"
    end
  end

  task :rebuild_docker do
    on roles(:all) do |h|
      execute "docker build -t grader #{fetch :deploy_to}/current/hacktester/docker/."
    end
  end

  task :restart_grader do
    on roles(:all) do |h|
      execute "sudo restart hacktester || sudo start hacktester"
    end
  end

  task :restart_celery do
    on roles(:all) do |h|
      execute "sudo restart celery || sudo start celery"
    end
  end

  after :published, :pip_install
  after :pip_install, :run_migrations
  after :run_migrations, :rebuild_docker
  after :run_migrations, :run_collect_static
  after :run_collect_static, :restart_grader
  after :restart_grader, :restart_celery
end
