import requests, json, datetime
from lxml import etree
from copy import deepcopy

def get(url):
    headers = {"Accept" : "application/xml"}
    resp = requests.get(url, headers=headers)
    xml = etree.fromstring(resp.text.encode("utf-8"))
    return xml
    
def get_project(identifier):
    raw = get("http://gtr.rcuk.ac.uk/project/" + identifier)
    return Project(raw)

"""
def get_fund(identifier):
    raw = get("http://gtr.rcuk.ac.uk/cerif/cffund/" + identifier)
    return Fund(raw['cfClassOrCfClassSchemeOrCfClassSchemeDescr'][0])
"""

def get_org(identifier):
    raw = get("http://gtr.rcuk.ac.uk/orgunit/" + identifier)
    return Org(raw)
    
def get_person(identifier):
    raw = get("http://gtr.rcuk.ac.uk/pers/" + identifier)
    return Person(raw)

def get_publication(identifier):
    raw = get("http://gtr.rcuk.ac.uk/publication/" + identifier)
    return Publication(raw)

class Native(object):
    def __init__(self, raw):
        self.raw = raw
    
    def from_xpath(self, xp):
        els = self.raw.xpath(xp)
        if els is not None and len(els) > 0:
            return els[0].text
        return None
        
    def xml(self):
        return etree.tostring(self.raw, pretty_print=True)

class Person(Native):
    def id(self):
        return self.from_xpath("/personOverview/person/id")
        
    def name(self):
        return self.from_xpath("/personOverview/person/name")
            
    def projects(self):
        projects = []
        for el in self.raw.xpath("/personOverview/projectOverviews"):
            root = etree.Element("projectOverview")
            for child in el:
                root.append(deepcopy(child))
            projects.append(Project(root))
        return projects

class Org(Native):
    def id(self):
        return self.from_xpath("/organisationOverview/organisation/id")
        
    def name(self):
        return self.from_xpath("/organisationOverview/organisation/name")
        

class Project(Native):
    def id(self):
        return self.from_xpath("/projectOverview/project/id")

    def title(self):
        return self.from_xpath("/projectOverview/project/title")
    
    def start(self):
        return self.from_xpath("/projectOverview/project/fund/start")
        
    def end(self):
        return self.from_xpath("/projectOverview/project/fund/end")
    
    def abstract(self):
        return self.from_xpath("/projectOverview/project/abstractText")
    
    def funder(self):
        return self.from_xpath("/projectOverview/project/fund/funder/name")
    
    def value(self):
        return self.from_xpath("/projectOverview/project/fund/value")
    
    def category(self):
        return self.from_xpath("/projectOverview/project/grantCategory")
    
    def reference(self):
        return self.from_xpath("/projectOverview/project/grantReference")
    
    def lead(self):
        os = []
        for org in self.raw.xpath("/projectOverview/leadResearchOrganisation"):
            id = org.xpath("id")[0].text
            name = org.xpath("name")[0].text
            os.append((id, name))
        return os
        
    def orgs(self):
        os = []
        for org in self.raw.xpath("/projectOverview/organisations"):
            id = org.xpath("id")[0].text
            name = org.xpath("name")[0].text
            os.append((id, name))
        return os
        
    def people(self):
        os = []
        for pers in self.raw.xpath("/projectOverview/coInvestigators"):
            id = pers.xpath("id")[0].text
            name = pers.xpath("name")[0].text
            os.append((id, name))
        for pers in self.raw.xpath("/projectOverview/principalInvestigators"):
            id = pers.xpath("id")[0].text
            name = pers.xpath("name")[0].text
            os.append((id, name))
        return os
        
    def outputs(self):
        os = []
        out = self.raw.xpath("/projectOverview/project/output")
        for child in out[0]:
            os.append(etree.tostring(child))
        return os
