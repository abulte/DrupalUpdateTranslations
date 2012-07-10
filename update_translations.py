from pprint import pprint
import os, sys, subprocess, urllib2, logging
from urllib2 import Request, urlopen, URLError, HTTPError

DRUPAL_ROOT = "/var/www/drupal"
DRUSH_PATH = "/usr/local/bin/drush"
BASE_TRANSLATION_URL = "http://ftp.drupal.org/files/translations/7.x"
CORE_VERSION = "7.14"
LANGUAGE_CODE = "fr"

class Utils:
	@staticmethod
	def getModuleDir(module):
		# drupal core
		if module == 'drupal':
			return DRUPAL_ROOT + '/profiles/standard'
	
		# other modules
		module_dir = DRUPAL_ROOT + '/sites/all/modules/' + module
		if not os.path.exists(module_dir):
			module_dir = module_dir = DRUPAL_ROOT + '/sites/all/modules/contrib/' + module
		if not os.path.exists(module_dir):
			return False
		return module_dir

	@staticmethod
	def downloadAndSaveFile(url, target_file):
		try:
			f = urllib2.urlopen(url)
			local_file = open(target_file, 'w')
			local_file.write(f.read())
			local_file.close()
			print "Done. Saved as %s." %target_file
		except HTTPError as e:
			print "HTTP Error:", e.code, url
		except URLError as e:
			print "URL Error:", e.reason, url
		except IOError as e:
			print "IO Error: %s" %e


## BEGIN

os.chdir(DRUPAL_ROOT)

# Drush command calls (modules lists)
p_raw = subprocess.Popen([DRUSH_PATH, 'pm-list', '--status=enabled', '--pipe', '--no-core'], shell=False, stdout=subprocess.PIPE)
cmd_modules_raw = p_raw.stdout.read()
p_detail = subprocess.Popen([DRUSH_PATH, 'pm-list', '--status=enabled', '--no-core'], shell=False, stdout=subprocess.PIPE)
cmd_modules_detail = p_detail.stdout.read()

modules_detail = cmd_modules_detail.split('\n')
modules_raw = cmd_modules_raw.split('\n')

titles = modules_detail[0]
# we dont need title line anymore
modules_detail.pop(0)

version_substr = titles.find("Version")

# get module versions from detailed list
# module machine name is fetched from raw list
modules_versions = []
for i in range(len(modules_detail)):
	if modules_raw[i] <> '':
		modules_versions.append({'version': modules_detail[i][version_substr:-1].strip(), 'module': modules_raw[i]})

## add core by hand
modules_versions.append({'version': CORE_VERSION, 'module': 'drupal'})
		
for m_v in modules_versions:
	translation_filename = '%s-%s.%s.po' % (m_v['module'], m_v['version'], LANGUAGE_CODE)
	url = '%s/%s/%s' % (BASE_TRANSLATION_URL, m_v['module'], translation_filename) 
	print "Fetching %s..." %url
	try:
		module_dir = Utils.getModuleDir(m_v['module'])
		if not module_dir:
			raise Warning('Module directory not found for module %s' %m_v['module'])
		module_dir += '/translations/'
		if not os.path.exists(module_dir):
			os.mkdir(module_dir)
		filename = module_dir + translation_filename
		Utils.downloadAndSaveFile(url, filename)
	except Warning as e:
	 	print "Warning: %s" %e
	
