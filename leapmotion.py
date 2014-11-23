import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
from selenium import webdriver
import Leap
import random
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from selenium.webdriver.common.keys import Keys


class SampleListener(Leap.Listener):
    
    browser = webdriver.Firefox()
    inComments = False
    subreddits = ['all', 'pics', 'gaming', 'onetruegod', 'onetruegod',  'onetruegod', 'onetruegod', 'onetruegod', 'onetruegod', 'adviceanimals', 'scoreball',  'gifs', 'aww', 'dataisbeautiful', 'natureporn', 'f7u12_ham', 'oldpeoplefacebook', 'funny', 'birdswalking', 'smashbros', 'iamverysmart']
    comments = ['Literally this', 'An upvote for you good sir', "Ctrl F'd for tree fiddy was not disappointed", 'Why are you guys downvoting this?', 'Nicolas Cage is the One True God', "This is bullshit - you're oversimplifying a complex situation to the point of no longer adding anything useful to the discussion.", "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead.",'Nicolas Cage is the One True God', 'Risky Click', 'Shots Fired', 'Nailed It', 'You I like you', 'Tree Fiddy', 'Nicolas Cage is the One True God', 'Circlejerk must be leaking', 'I have the weirdest boner right now', "Step one be attractive, step two don't be unattractive", 'Nicolas Cage is the One True God', 'Are you me?', 'Is your girlfriend single?', 'Nicolas Cage is the One True God', 'holds up spork', 'boy that escalated quickly', 'relevant xkcd', 'Damn onions', 'u wot m8', 'I tip my hat to you good sir']
    
    
    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.config.set("Gesture.Circle.MinRadius", 40.0)
        controller.config.set("Gesture.Swipe.MinLength", 200.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 50)
        controller.config.save()
        self.browser.get("http://redditp.com")
        checkbox = self.browser.find_element_by_id('autoNextSlide')
        
        checkbox.click()
        print "Connected"
        
     
    def on_frame(self, controller):
        frame = controller.frame()
        for gest in frame.gestures():
            if(gest.type == Leap.Gesture.TYPE_SWIPE):
                swipe = SwipeGesture(gest)
                print "swipe", swipe.direction
                if(swipe.direction[0] > .5):
                    right = self.browser.find_element_by_id('nextButton')
                    right.click()
                elif(swipe.direction[0] < -.5):
                    if(self.inComments):
                        self.browser.back()
                        self.inComments=False
                    else:
                        left = self.browser.find_element_by_id('prevButton')
                        left.click()
                elif(swipe.direction[1] > .5 and self.inComments):
                    table = self.browser.find_element_by_xpath('//body')
                    for i in range(10):
                        table.send_keys(Keys.DOWN)
    
                elif(swipe.direction[1] < -.5 and self.inComments):
                    table = self.browser.find_element_by_xpath('//body')
                    for i in range(10):
                        table.send_keys(Keys.UP)
    
                    
            elif(gest.type == Leap.Gesture.TYPE_SCREEN_TAP and not self.inComments):
                print "Poke"
                self.inComments=True
                comments = self.browser.find_element_by_id('navboxCommentsLink')
                comments.click()
                try:
                        print "Logging in"
                        username = self.browser.find_element_by_name('user')
                        username.send_keys('pyLeap')
                        password = self.browser.find_element_by_name('passwd')
                        password.send_keys('hunter2')
                        button = self.browser.find_element_by_xpath('//*[@id="login_login-main"]/div[3]/button')
                        button.click()
                except:
                        print "Already Logged in"
          
            elif(gest.type == Leap.Gesture.TYPE_CIRCLE):
                circle = Leap.CircleGesture(gest)
                print "Circle", circle.radius
                if (not self.inComments):
                    index = random.randint(0, len(self.subreddits)-1)
                    self.browser.get('redditp.com/r/'+self.subreddits[index])
                print "Circle Done"
            elif(gest.type == Leap.Gesture.TYPE_KEY_TAP):
                print "Key Tap"
                textbox = self.browser.find_element_by_name('text')
                index = random.randint(0, len(self.comments)-1) 
                textbox.send_keys(self.comments[index]+"\n")
                


def main():
    controller = Leap.Controller()
    listener = SampleListener()
    
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()