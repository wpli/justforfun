
# coding: utf-8

## How many people have done the #ALS #IceBucketChallenge?

#### An [IPython Notebook](http://ipython.org/notebook.html) Analysis of the Viral Internet

# by [William Li](https://twitter.com/williampli) 

### Most Importantly...

# Please consider making a donation to the [ALS Association](http://www.alsa.org/) in support of research. 
# 
# Another related organization worth learning about is the [ALS Residence Initiative (ALSRI)](http://www.alsri.org/), created by my friend, Steve Saling. The ALSRI creates technology-equipped residences so that people with ALS have access to all of the technology required to survive ALS for the rest of their life with the highest level of mobility and independence possible.
# 
# This film, [Jon Imber's Left Hand](http://vimeo.com/91172268), is also worth watching. [Jon Imber](http://www.bostonglobe.com/metro/2014/04/24/jon-imber-artist-kept-painting-with-exuberance-face-als/bQen0EjAUKD2veEeXwPvpL/story.html) was an artist diagnosed with ALS who lived an amazing life. He passed away earlier this year.

### Some Quick Simulations

# Just for fun, it might be interesting to see how the ALS Ice Bucket Challenge spreads. According to Wikipedia, the challenge started roughly on July 15, 2014. For our first model, we'll assume:
# 
# * there was one person who started it all
# * each person who participates challenges three people
# * of the three people who are challenged, two of them accept the challenge
# 
# My main simulation suggests that 3.9 million people have done the ALS Ice Bucket Challenge.

# In[78]:

num_starters = 1
num_challengers = 3
num_accepting = 2
people_per_day = []

import datetime
start_date = datetime.date( 2014,7,15 )

today = datetime.date.today()

num_days_timedelta = today - start_date
num_days = num_days_timedelta.days
for i in range( num_days ):
    people_per_day.append( num_starters * num_accepting**i ) 

print "Number of days: %s" % num_days
print sum( people_per_day )


# OK, 68.7 billion people is, well, a lot. For completeness, it's worth noting what happens if 0, 1, 2, or all 3 people participate in the challenge: 
# 

# In[35]:


people_per_day = []

for num_accepting in [ 0, 1, 2, 3 ]:
    for i in range( num_days ):
        people_per_day.append( num_starters * num_accepting**i ) 

    print "If %s people accept, the total number of people who accept are:" % num_accepting, 
    print sum( people_per_day )


# Of course, 68.7 billion or 75 quadrillion people are estimates that are far too high. Also, it seems like more than 37 of my Facebook friends have done the Ice Bucket Challenge already. A better model is needed.

### Model #2: A Random Number of People Accepting Your Challenge

# Perhaps we can refine our model of the ALS Ice Bucket Challenge as follows: Instead of a fixed number of people who accept the challenge, there is an equal chance that 0, 1, 2, or 3 of a participant's challengers will accept (25% for each number)
# 
# I've simulated this below. Because there is randomness, we need to simulate multiple times and look at the distribution of number of participants (someone, let me know if this qualifies as a "Monte Carlo simulation").

# In[124]:

import random

possible_acceptances = [0,1,2,3]

num_iterations = 100

one_starter_total_participants_per_iteration = []

for iteration in range( num_iterations ):
    people_per_day = []
    for i in range(num_days):
        if i == 0:
            # start with 1 person
            people_per_day.append( 1 )
        else:

            day_sum = 0        
            for participant in range( people_per_day[i-1] ):
                day_sum += random.choice( possible_acceptances )

            #print i, day_sum
            people_per_day.append( day_sum )
            
    total_participants = sum( people_per_day )
    print "Run %s | Participants: %s" % ( iteration, total_participants )
    one_starter_total_participants_per_iteration.append( total_participants )
        


# That's a lot of variance over the simulated run -- between 1 and 20 million (the theoretical maximum was 75 quadrillion). It turns out that the number of participants in certain simulations (about 25% of them!) is exactly 1 --- no one accepts the first challenger.
# 
# I've summarized and plotted the results below. The average number of participants in these simulations is 3.9 million. This might be a realistic number, in light of the fact that the ALS Association recently announced that [it has raised $22.9 million](http://www.alsa.org/news/media/press-releases/ice-bucket-challenge-081914.html), this might be a realistic estimate.

# The estimated average number of participants is quite high: 22.5 million. The variance has reduced, since there are far fewer cases where no one after day 1 does the challenge. 
# 
# The results from this model are summarized below. The histogram is more normally distributed (Gaussian), since there are fewer very-low events). Overall, the average estimate in this case, though, is arguably too high; I leave the tweaking of parameters and better models to future work (please [fork the code](https://github.com/wpli/justforfun) if you're interested!)

# In[131]:

import numpy
print "Average Number of Participants: %s" % int( numpy.round( numpy.mean( multiple_starters_total_participants_per_iteration ) ) )
print "Standard Deviation of Number of Participants: %s" % int( numpy.round( numpy.std( multiple_starters_total_participants_per_iteration ) ) )
print "Minimum: %s" % int( numpy.round( numpy.min( multiple_starters_total_participants_per_iteration ) ) )
print "Maximum: %s" % int( numpy.round( numpy.max( multiple_starters_total_participants_per_iteration ) ) )

hist( multiple_starters_total_participants_per_iteration )
title( "Histogram of Simulated Number of Participants" )
xlabel( "Number of Participants" )
ylabel( "Count (out of %s simulations)" % num_iterations ) 


### Future Work

# This model could be extended in many ways. It'd be interesting to study actual data associated with the Ice Bucket Challenge (e.g. on Twitter and Facebook) and see how many people actually learned about ALS. The actual impact of the challenge on donations in support of people with ALS would also be worthwhile research. 
# 
# A final, personal plug: This fall, I'm co-teaching a course at MIT called [6.811: Principles and Practice of Assistive Technology](http://courses.csail.mit.edu/PPAT). Small teams of students work with people with disabilities over an entire semester and develop customized devices and solutions that help them live more independently. In previous years, we have worked with people with ALS in the Boston area, including the aforementioned Steve Saling. Please visit the [course website](http://courses.csail.mit.edu/PPAT), join our "friends" mailing list, or get in touch with me ([@williampli](http://www.twitter.com/williampli) or [wli@csail.mit.edu](mailto:wli@csail.mit.edu)) to learn more. 

### Extension: Model #3 More than One Starter (A Tiny Refinement)

# In[128]:

import random

possible_acceptances = [0,1,2,3]

num_iterations = 100

num_starters = 5
multiple_starters_total_participants_per_iteration = []

for iteration in range( num_iterations ):
    people_per_day = []
    for i in range(num_days):
        if i == 0:
            # start with 1 person
            people_per_day.append( num_starters )
        else:

            day_sum = 0        
            for participant in range( people_per_day[i-1] ):
                day_sum += random.choice( possible_acceptances )

            #print i, day_sum
            people_per_day.append( day_sum )
            
    total_participants = sum( people_per_day )
    print "Run %s | Participants: %s" % ( iteration, total_participants )
    multiple_starters_total_participants_per_iteration.append( total_participants )
        


# Having one starter results in a substantial chance (25%, in our case) that only one person will do the challenge --- the viral dynamics of the Internet won't take off. It seems like the ALS Ice Bucket Challenge had, at various stages, multiple people join without being challenged (maybe they self-nominated). One approximation is that we assume that five people, not one person, started the challenge, and use the same approach as above:

# In[132]:

import numpy
print "Average Number of Participants: %s" % int( numpy.round( numpy.mean( one_starter_total_participants_per_iteration ) ) )
print "Standard Deviation: %s" % int( numpy.round( numpy.std( one_starter_total_participants_per_iteration ) ) )
print "Maximum: %s" % int( numpy.round( numpy.min( one_starter_total_participants_per_iteration ) ) )
print "Minimum: %s" % int( numpy.round( numpy.max( one_starter_total_participants_per_iteration ) ) )

hist( total_participants_per_iteration )
title( "Histogram of Simulated Number of Participants" )
xlabel( "Number of Participants" )
ylabel( "Count (out of %s simulations)" % num_iterations ) 

