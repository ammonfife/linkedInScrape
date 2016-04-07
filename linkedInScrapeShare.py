########################################################################################################################
## LinkedIn Skill Scraper
## Because Hello World was too boring
## @ammonfife
## https://www.linkedin.com/in/ammonfife
## First script with python, so don't judge
## Script will not work without a linkedIn email address and password
########################################################################################################################


#Works/built with Python 2.7.11 - Will not run with Python 3 interpreters
#I also have IPython 4.1.2 running

# Load packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import base64
#import csv #csvkit handles Unicode better
import csvkit


needLogin = True

#You will need to change the location for your driver, or leave it blank, and comment out the set_preference fields to use default, but you may run into long waits for tags to load that you don't need.
firefoxProfile = webdriver.FirefoxProfile('/Users/afife/Library/Application Support/Firefox/Profiles/3nzmyfpr.Automation')
driver = webdriver.Firefox(firefoxProfile) # open Firefox browser


#firefoxProfile = webdriver.FirefoxProfile('/Users/afife/Library/Application Support/Firefox/Profiles/3nzmyfpr.Automation')
firefoxProfile.set_preference('permissions.default.stylesheet', 2)
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
firefoxProfile.set_preference("http.response.timeout", 10)
firefoxProfile.set_preference("dom.max_script_run_time", 10)

#If statement was only needed for testing, but I kept it here anyway, if I need to debug again and don't want to log in over and over.
if needLogin:
    #Login

    driver.get('https://www.linkedin.com/uas/login')
    emailfield = driver.find_element_by_id('session_key-login')

    #I encoded my email and password so it's not plainly obvious to people over my shoulder, (didn't want to have to change my password), you can either encode your email and password using
    print base64.b64encode('youremailaddress@gmail.com') + " <-- paste this output into emailfield.send_keys(base64.b64decode(HERE))"
    #and paste it below, or just put it in plain and ditch the base64 function
    emailfield.send_keys(base64.b64decode("ZW1haWxAZ21haWwuY29t"))
    pwdfield = driver.find_element_by_id('session_password-login')
    # I encoded my email and password so it's not plainly obvious to people over my shoulder, (didn't want to have to change my password), you can either encode your email and password using
    print base64.b64encode('y0u4P@s$woRd!') + " <-- paste this output into pwdfield.send_keys(base64.b64decode(HERE))"
    # and paste it below, or just put it in plain and ditch the base64 stuff
    pwdfield.send_keys(base64.b64decode("eTB1NFBAcyR3b1JkIQ=="))


    #Login
    login_button = driver.find_element_by_id('btn-primary')
    login_button.click()
    time.sleep(5) # delays for 5 seconds

else:
    print "continue"
#Start Search


#companyName can also be keywords
companyName = 'maxpoint'
baseSearchUrl = 'https://www.linkedin.com/vsearch/p?keywords='
keywordSearchUrl = baseSearchUrl + companyName

#keyword override
#keywordSearchUrl = 'https://www.linkedin.com/vsearch/f?orig=QRYRW&keywords=boncom+analytics&pt=people&queryRewriteParams=1'


#loop through people

pleaseContinue = True
loopBreaker = 1

#not really using this 'while not' loop anymore, but it's still  here. Was using it to paginate results pages until there were no more. I'd remove it from the code, but i'm currently blocked from linkedIn, so can't test the code if I change it.
while not pleaseContinue == False:


    #Rather than looking for the next button, I changed the code to just iterate 1-100, and fail when done
    for searchResult in range(1, 100):
        keywordSearchUrl = 'https://www.linkedin.com/vsearch/p?&keywords='& str(companyName) &'&queryRewriteParams=1&page_num=' +str(searchResult) +'&pt=people&openFacets=N,G,CC'

        #Override to explicitly include only current maxpoint employees, comment line out to return to above
        'https://www.linkedin.com/vsearch/p?orig=QRYRW&keywords=maxpoint&f_CC=9744597%2C503560&page_num=' +str(searchResult) +'&queryRewriteParams=1'
        #keywordSearchUrl = 'https://www.linkedin.com/vsearch/p?type=people&keywords=ammon&orig=GLHD&rsid=125370481460006577728&pageKey=voltron_people_search_internal_jsp&trkInfo=tarId%3A1460006582537&search=Search'
        driver.get(keywordSearchUrl)
        time.sleep(5)  # delays for 5 seconds


        #move to end
        try:

            for searchResult in range(1, 11):
                print "We're on iteration %d" % searchResult
                time.sleep(1)  # delays for 1 seconds

                try:
                    resultPeople = driver.find_element_by_xpath('//*[@id="results"]/li[' + str(searchResult) + ']/div/h3/a')
                    pName = resultPeople.text
                    print resultPeople.text
                except:
                    print "no name"
                    pName = "Error"


                main_window = driver.current_window_handle

                # resultPeople.click()
                resultPeople.send_keys(Keys.COMMAND + Keys.SHIFT + Keys.RETURN)
                time.sleep(5)  # delays for 5 seconds

                driver.switch_to_window(driver.window_handles[0])
                linkedInURL = driver.find_element_by_class_name("view-public-profile")
                pURL = linkedInURL.text
                print linkedInURL.text

                #Can probably remove
                body = driver.find_element_by_tag_name("body")

                #Preset variables to prevent exceptions on nulls
                pastCompany1 = ""
                pastCompany2 = ""
                pastCompany3 = ""
                currentCompany = ""
                currentCompany2 = ""
                currentCompany3 = ""
                pRecommendationsReceived=""
                pRecommendationsGiven=""
                currentCompany=""
                currentCompany2=""
                currentCompany3=""
                astCompany1=""
                pastCompany2=""
                pastCompany3=""
                Education1 =""



                try:
                    pRecommendReceived = driver.find_element_by_xpath('//*[@id="endorsements"]/ul/li[1]/a')
                    if pRecommendReceived.is_displayed():
                        # print recommendReceived.text
                        pRecommendationsReceived = re.compile('\(([^\)]*)\)*').search(pRecommendReceived.text).group(1)
                        print "recommendations"
                        print pRecommendationsReceived


                    else:
                        print "recommendations"
                        print 0
                except:
                    print "recommendations"
                    print 0

                try:
                    recommendGiven = driver.find_element_by_xpath('//*[@id="endorsements"]/ul/li[2]/a')
                    if recommendGiven.is_displayed():
                        # print recommendReceived.text
                        pRecommendationsGiven = re.compile('\(([^\)]*)\)*').search(recommendGiven.text).group(1)
                        print "recommendations Given"
                        print pRecommendationsGiven

                    else:
                        #removed :
                        print 0
                except:
                    print "recommendations Given"
                    print 0

                # Current Company
                try:
                    currentCompany = driver.find_element_by_xpath(
                        '//*[@id="overview-summary-current"]/td/ol/li/span/strong/a').text
                    print currentCompany
                except:
                    xfg46dg = 1

                try:
                    currentCompany2 = driver.find_element_by_xpath(
                        '//*[@id="overview-summary-current"]/td/ol/li[2]/span/strong/a').text
                    print currentCompany2
                except:
                    xfg46dg = 1

                try:
                    currentCompany3 = driver.find_element_by_xpath(
                        '//*[@id="overview-summary-current"]/td/ol/li[3]/span/strong/a').text
                    print currentCompany3
                except:
                    xfg46dg = 1

                # Past Company




                try:
                    pastCompany1 = driver.find_element_by_xpath('//*[@id="overview-summary-past"]/td/ol/li[1]/a').text
                    print pastCompany1
                except:
                    try:
                        pastCompany1 = driver.find_element_by_xpath(
                            '//*[@id="overview-summary-past"]/td/ol/li[1]/span/strong/a').text
                        print pastCompany1
                    except:
                        print "no past company1"
                try:
                    pastCompany2 = driver.find_element_by_xpath('//*[@id="overview-summary-past"]/td/ol/li[2]/a').text
                    print pastCompany2
                except:
                    try:
                        pastCompany2 = driver.find_element_by_xpath(
                            '//*[@id="overview-summary-past"]/td/ol/li[2]/span/strong/a').text
                        print pastCompany2
                    except:
                        print "no company 2"
                try:
                    pastCompany3 = driver.find_element_by_xpath('//*[@id="overview-summary-past"]/td/ol/li[3]/a').text
                    print pastCompany3
                except:
                    try:
                        pastCompany3 = driver.find_element_by_xpath(
                        '//*[@id="overview-summary-past"]/td/ol/li[3]/span/strong/a').text
                        print pastCompany3
                    except:
                        print 'no company3'

                # Education
                try:
                    Education1 = driver.find_element_by_xpath('//*[@id="overview-summary-education"]/td/ol/li/a')
                    print Education1.text
                    Education1 = Education1.text
                except:
                    k956568545fgh = 3

                # Create individual static properties
                profileInfo = [pName, pURL, pRecommendationsReceived, pRecommendationsGiven, currentCompany,
                               currentCompany2, currentCompany3, pastCompany1, pastCompany2, pastCompany3, Education1]
                print(profileInfo)

                # Gather Skills and Iterate

                try:
                    expandSkills = driver.find_element_by_class_name('more-text')
                    print "works"

                    if expandSkills.is_displayed():
                        try:
                            driver.execute_script("return arguments[0].scrollIntoView();", expandSkills)
                            expandSkills.send_keys(Keys.ARROW_UP)
                            expandSkills.send_keys(Keys.ARROW_UP)
                            time.sleep(1)  # delays for 1 seconds
                            expandSkills.click()
                            time.sleep(1)  # delays for 1 seconds
                        except:
                            print "hmm"

                    else:
                        print "no more skills"

                except:
                    print "Not enough skills"

                for topSkills in range(1, 11):
                    try:
                        # endorsecount goes 1-10

                        newRow = list(profileInfo)
                        newRow.append(topSkills)

                        try:
                            endorseName = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[1]/li[' + str(topSkills) + ']/span/span/a')
                            if endorseName.is_displayed():
                                print endorseName.text
                                newRow.append(endorseName.text)
                            else:
                                newRow.append("")
                                print ""
                        except:
                            print "no skill " + str(topSkills)
                            newRow.append("")
                        try:
                            endorseCount = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[1]/li[' + str(topSkills) + ']/span/a/span')
                            if endorseCount.is_displayed():

                                if endorseCount.text is None:
                                    endorseCount.text = 0

                                print endorseCount.text
                                newRow.append(endorseCount.text)
                            else:
                                newRow.append("")
                                print 0
                        except:
                            print 0

                        # Save New Row
                        print newRow
                        f = open('csvOutput copy.csv', 'a')
                        try:
                            writer = csvkit.writer(f)
                            writer.writerow(newRow)

                        except:
                            print"could not write row"

                        finally:
                            f.close()


                    except:
                        print "messed up skills"
                # 2 goes 1-40


                for otherSkills in range(1, 41):
                    # endorsecount goes 1-10
                    newRow = list(profileInfo)
                    newRow.append(otherSkills + 10)
                    try:

                        try:
                            endorseName2 = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[2]/li[' + str(otherSkills) + ']/div/span/span/a')
                            if endorseName2.is_displayed():
                                print endorseName2.text
                                newRow.append(endorseName2.text)
                            else:
                                print ""
                                print"no more skills, moving on"


                                # newRow.append("")

                        except:
                            endorseName2 = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[2]/li[' + str(otherSkills) + ']/div/span/a')
                            if endorseName2.is_displayed():
                                print endorseName2.text
                                newRow.append(endorseName2.text)
                            else:
                                print ""
                                print"no more skills, moving on"
                                # break
                                newRow.append("")

                        try:
                            endorseCount = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[2]/li[' + str(otherSkills) + ']/div/span/a/span')
                            if endorseCount.is_displayed():
                                print endorseCount.text
                                newRow.append(endorseCount.text)
                            else:
                                print 0
                                newRow.append(0)
                        except:
                            endorseCount = driver.find_element_by_xpath(
                                '//*[@id="profile-skills"]/ul[2]/li[' + str(otherSkills) + ']/div/span/span/a')
                            if endorseCount.is_displayed():
                                print endorseCount.text
                                newRow.append(endorseCount.text)
                            else:
                                print 0
                                newRow.append(0)

                    except:
                        print "no skill " + str(otherSkills)
                        print"no more skills, moving on"
                        newRow = profileInfo
                        break

                    # Add Skill row to CSV
                    print newRow
                    f = open('csvOutput copy.csv', 'a')
                    try:
                        writer = csvkit.writer(f)
                        writer.writerow(newRow)

                    finally:
                        f.close()

                    newRow = list(profileInfo)

                print "success on " + pName + " move on"
                #


                # close new tab
                linkedInURL.send_keys(Keys.COMMAND + "w")
                # Loop to next Name

                f = open('csvOutput copy.csv', 'a')
                try:
                    writer = csvkit.writer(f)
                    print open('csvOutput copy.csv', 'rt').read()
                finally:
                    f.close()

            main_window = driver.current_window_handle

            print loopBreaker
            loopBreaker = loopBreaker +1
            if loopBreaker == 50:
                print "breaking"
                pleaseContinue = False
                break
        except:
            print 'no more pages'
            #continue
            #PleaseContinue = False


#close window
driver.quit()