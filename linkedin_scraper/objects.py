class Institution(object):
    institution_name = None
    website = None
    industry = None
    type = None
    headquarters = None
    company_size = None
    founded = None

    def __init__(self, name=None, website=None, industry=None, type=None, headquarters=None, company_size=None,
                 founded=None):
        self.name = name
        self.website = website
        self.industry = industry
        self.type = type
        self.headquarters = headquarters
        self.company_size = company_size
        self.founded = founded


class Experience(Institution):
    position_title = None

    def __init__(self,  position_title=None):
        self.position_title = position_title

    def __repr__(self):
        return "{position_title}  {company}".format( position_title=self.position_title,company=self.institution_name)


class Education(Institution):
    degree = None

    def __init__(self, degree=None):
        self.degree = degree

    def __repr__(self):
        return "{degree}".format(degree=self.degree)


class Skills:
    name = None

    def __init__(self, name = None):
        self.name=name

    def __repr__(self):
        return self.name


class Scraper(object):
    driver = None

    def is_signed_in(self):
        try:
            self.driver.find_element_by_id("profile-nav-item")
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element_by_xpath(tag_name)
            return True
        except:
            pass
        return False






