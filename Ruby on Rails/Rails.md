## Create New App
* Run: <code>rails new <app_name></code>
    - this command automatically runs <code>bundle install</code>
* Use <code>bundle install</code> to install gems specified in Gemfile.
    - <code>bundle install --without production</code> doesn't install the gems under production group
* <code>bundle update</code> updates gems already installed; good if you changed the version of a gem in Gemfile.

## Run Locally
* <code>rails server</code> 

---
+ `generate`:generates Ruby on Rails scaffolding.
    * EX: `rails generate controller <controller name> <controller actions>`
    * `rails g` shortcut
    * `rails destroy controller <controller name> <controller actions>` undos generate command

---
+ `bundle exec rake test`: runs Rails tests in `test` directory of app