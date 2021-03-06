## map from descriptive name to list of JBIDE and/or JBDS components in JIRA.
JIRA_components = {
    "Aerogear          ": { "aerogear-hybrid", "cordovasim" },
    "Arquillian        ": { "arquillian" },
    # "Error Reporting " : {"aeri"},
    "Base              ": { "common", "foundation", "usage" },
    # "Batch           ": { "batch"},
    "BrowserSim        ": { "browsersim" },
    "build, ci, maven-plugins": { "build" },
    "build-sites       ": { "updatesite" },
    "Central           ": { "central", "maven", "project-examples" },
    # "CDI             " : { "cdi"},
    "Discovery         ": { "central-update" },
    # "Docker          ": { "docker" },
    "dl.j.o, devdoc    ": { "website" },
    # "Easymport       ": { "easymport" },
    "Forge             ": { "forge" },
    "Freemarker        ": { "freemarker" },
    "Hibernate         ": { "hibernate"},
    "Integration-Tests ": { "qa" },
    "JavaEE            ": { "jsf", "seam2", "cdi", "cdi-extensions", "jsp/jsf/xml/html-source-editing"},
    # "javascript      ": { "javascript", "nodejs"},
    "JST               ": { "jst"},
    "LiveReload        ": { "livereload" },
    # "Maven           ": { "maven"},
    "OpenShift         ": { "openshift", "cdk" },
    # "Project Examples": { "project-examples"},
    "Server            " : {  "server", "archives", "jmx" },
    # "Usage Analytics " : { "usage"},
    "versionwatch      ": { "versionwatch" },
    "VPE               ": { "visual-page-editor-core", "visual-page-editor-templates"},
    "Webservices       ": { "webservices"}
    }

# there are more N&N pages than there are JIRA components (eg., jbosstools-central includes Central, Maven and Project Examples) so this list is a bit different from teh above one
# # first component listed in the set will be the one used to assign the JIRA
NN_components = {
    "Aerogear          ": { "aerogear-hybrid", "cordovasim" },
    "Arquillian        ": { "arquillian" },
    "Error Reporting   " : {"aeri"},
    "Base              ": { "common", "foundation", "usage" },
    "Batch             ": { "batch"},
    "BrowserSim        ": { "browsersim" },
    # "build, ci, maven-plugins": { "build" },
    # "build-sites     ": { "updatesite" },
    "Central           ": { "central", "maven", "project-examples" },
    "CDI               ": { "cdi"},
    # "Discovery       ": { "central-update" },
    "Docker            ": { "docker" },
    # "dl.j.o, devdoc  ": { "website" },
    "Easymport         ": { "easymport" },
    "Forge             ": { "forge"},
    "Freemarker        ": {"freemarker"},
    "Hibernate         ": { "hibernate"},
    # "Integration-Tests": { "qa" },
    # "JavaEE          ": { "jsf", "seam2", "cdi", "cdi-extensions" },
    "Javascript        ": { "javascript", "nodejs"},
    "JSF               ": { "jsp/jsf/xml/html-source-editing", "jsf"},
    "JST               ": { "jst"},
    "LiveReload        ": { "livereload" },
    "Maven             ": { "maven"},
    "OpenShift         ": { "openshift", "cdk" },
    "Project Examples  ": { "project-examples"},
    "Server            " : {  "server", "archives", "jmx" },
    "Usage Analytics   " : { "usage"},
    # "versionwatch    ": { "versionwatch" },
    "Visual Editor     ": { "visual-page-editor-core", "visual-page-editor-templates"},
    "Webservices / Rest": { "webservices"}
    }

def checkFixVersionsExist (jbide_fixversion, jbds_fixversion, jiraserver, username, password):
    import requests, re, urllib
    from requests.auth import HTTPBasicAuth

    # should never happen
    if jbide_fixversion is None:
        print "\n[ERROR] JBIDE fixversion " + jbide_fixversion + " can not be None\n"
        return False

    # verify that fixversions are valid and exist on the target jira server
    if jbds_fixversion is not None:
        testFixVersionsExistQuery = '((project IN (JBIDE) AND fixVersion = "' + jbide_fixversion + '") AND (project IN (JBDS) AND fixVersion = "' + jbds_fixversion + '"))'
    else:
        testFixVersionsExistQuery = 'project IN (JBIDE) AND fixVersion = "' + jbide_fixversion + '"'
    # print "\n" + 'Search for JIRAs in JBIDE ' + jbide_fixversion + ' and JBDS ' + jbds_fixversion + ":\n\n * " + jiraserver + \
    #   '/issues/?jql=' + urllib.quote_plus(testFixVersionExistsSearchquery) + \
    #   " * https://issues.stage.jboss.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?tempMax=1000&jqlQuery=" + \
    #   urllib.quote_plus(testFixVersionExistsSearchquery)
    q = requests.get(jiraserver + '/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?tempMax=1000&jqlQuery=' + \
        urllib.quote_plus(testFixVersionsExistQuery), \
        auth=HTTPBasicAuth(username, password), verify=False)
    # check for string: The value '4.4.7.foo' does not exist for the field 'fixVersion'
    if re.search("The value '" + jbide_fixversion + "' does not exist for the field 'fixVersion'", q.text):
       print "\n[ERROR] JBIDE fixversion " + jbide_fixversion + " does not exist on " + jiraserver + "\n"
       return False
    elif jbds_fixversion is not None and re.search("The value '" + jbds_fixversion + "' does not exist for the field 'fixVersion'", q.text):
       print "\n[ERROR] JBDS fixversion " + jbds_fixversion + " does not exist on " + jiraserver + "\n"
       return False
    else:
        return True

# default assignee if can't find one in JIRA
def defaultAssignee():
    return "jeffmaury"

def queryComponentLead (componentList, componentID, nameOrDisplayName):
    # print "Search for component lead of " + projectID+":"+componentID+" on "+jiraserver+"..."
    for c in componentList:
        # print c.name
        if c.name == componentID:
            if nameOrDisplayName == 1:
                return c.lead.displayName # pretty name
            else:
                return c.lead.name # ID
    # if component not found, return default assignee
    return defaultAssignee()
# examples
# jira = JIRA(options={'server':jiraserver}, basic_auth=(options.usernameJIRA, options.passwordJIRA))
# print queryComponentLead(jira.project_components(jira.project('JBIDE')), 'build', 0)
# print queryComponentLead(jira.project_components(jira.project('JBIDE')), 'build', 1)
