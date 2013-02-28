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
    raw = get("http://gtr.rcuk.ac.uk/organisation/" + identifier)
    return Org(raw)
    
def get_person(identifier):
    raw = get("http://gtr.rcuk.ac.uk/person/" + identifier)
    return Person(raw)

def get_publication(identifier):
    raw = get("http://gtr.rcuk.ac.uk/publication/" + identifier)
    return Publication(raw)

class Native(object):
    def __init__(self, raw):
        self.raw = raw
    
    def from_xpath(self, xp):
        els = self.raw.xpath(xp, namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"})
        if els is not None and len(els) > 0:
            return els[0].text
        return None
        
    def xml(self):
        return etree.tostring(self.raw, pretty_print=True)

class Person(Native):
    def id(self):
        return self.from_xpath("/gtr:personOverview/gtr:person/gtr:id")
        
    def name(self):
        return self.from_xpath("/gtr:personOverview/gtr:person/gtr:name")
            
    def projects(self):
        projects = []
        for el in self.raw.xpath("/gtr:personOverview/gtr:projectOverviews", namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"}):
            root = etree.Element("{http://gtr.rcuk.ac.uk/api}projectOverview")
            for child in el:
                root.append(deepcopy(child))
            projects.append(Project(root))
        return projects

class Org(Native):
    def id(self):
        return self.from_xpath("/gtr:organisationOverview/gtr:organisation/gtr:id")
        
    def name(self):
        return self.from_xpath("/gtr:organisationOverview/gtr:organisation/gtr:name")
        

class Project(Native):
    def id(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:id")

    def title(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:title")
    
    def start(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:fund/gtr:start")
        
    def end(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:fund/gtr:end")
    
    def abstract(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:abstractText")
    
    def funder(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:fund/gtr:funder/gtr:name")
    
    def value(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:fund/gtr:valuePounds")
    
    def category(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:grantCategory")
    
    def reference(self):
        return self.from_xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/gtr:grantReference")
    
    def _get_id_name(self, parent_xpath):
        os = []
        for org in self.raw.xpath(parent_xpath, namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"}):
            id_el = org.xpath("gtr:id", namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"})
            id = None
            if id_el is not None and len(id_el) > 0:
                id = id_el[0].text
            name_el = org.xpath("gtr:name", namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"})
            name = None
            if id_el is not None and len(name_el) > 0:
                name = name_el[0].text
            os.append((id, name))
        return os
    
    def lead(self):
        return self._get_id_name("/gtr:projectOverview/gtr:projectComposition/gtr:leadResearchOrganisation")
        
    def orgs(self):
        return self._get_id_name("/gtr:projectOverview/gtr:projectComposition/gtr:organisations/gtr:organisation")
        
    def people(self):
        os = self._get_id_name("/gtr:projectOverview/gtr:projectComposition/gtr:projectPeople/gtr:projectPerson")
        # os2 = self._get_id_name("/gtr:projectOverview/gtr:projectComposition/gtr:projectPeople/gtr:principalInvestigators")
        return os # + os2
        
    def outputs(self):
        os = []
        out = self.raw.xpath("/gtr:projectOverview/gtr:projectComposition/gtr:project/output", namespaces={"gtr" : "http://gtr.rcuk.ac.uk/api"})
        if out is None or len(out) == 0: 
            return os
        for child in out[0]:
            os.append(etree.tostring(child))
        return os
