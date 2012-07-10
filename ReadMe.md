# Drupal Translations Download

## The problem
As of July 2012, Drupal (up to v7) can't handle proxy : <http://drupal.org/node/7881>. This is a big problem, especially when trying to update/fetch module translations (`l10n_update` module) through a proxy.

## The solution
**This is not a solution**, this is pretty much an ugly and limited workaround. For a solution, watch for Drupal 8 or issue #7881 commit in Drupal 7.

## The script
`updated_translations.py` lets you download your enabled modules translations into the `translations` subdirectory of the modules. It also works with core and downloads its translation in `profiles/standard/translations`.

## Requirements
* `Drush` (to get the list of enabled modules)
* `Python` (script was built on 2.7, tested on 2.6)
* Modules should be in `sites/all/modules/\*` or in `site/all/modules/contrib/\*`


## How to
* Place the `updated_translations.py` script wherever you want
* Edit the following variables :
	* DRUPAL_ROOT : root of your Drupal installation
	* DRUSH_PATH : complete path to Drush binary
	* BASE_TRANSLATION_URL : this should be OK as is
	* CORE_VERSION : your Drupal Core version
	* LANGUAGE_CODE : your language code
* Ensure your system is configured to use your proxy (urllib2 auto detects it), for example by setting the `http_proxy`variable
* Run the script as Web server user (root is OK too but not recommended), or at least with a user with write access in the modules directories : `python update_translations.py`
* In Drupal, delete the language you want to update (**WARNING** : this will erase your custom translations strings!!) and add it again so the translations files get fed into the system


## Improve
Feel free to propose improvements, Github is made for this! This script is just a quick workaround (and intended so) for now.