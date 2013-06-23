## Huh? The Reckoner!?

Yes, The Reckoner!  The Thunderdome for Decisions!  The Ultimate Arbiter for the Connected World!  And it's soft underbelly is made available to you, the fans, the curious, the intrigued!

The Reckoner was a web project I built in the Fall of 2011 that was built on one simple concept:

* Got a binary question?
* Good or bad?  
* Yes or no?  
* Happy Days better with Chachi or without Chachi?  

Put it on the Reckoner and let the world decide!
 
Essentially, people submit questions with two possible answers, the questions get approved and spruced up, and posted on the site for a week.  At the end of the week, you have your answer.  This was always intended as a toy, but a *fun* toy, and sometimes fun toys have a way of ingratiating themselves into a lot of people's lives in a satisfying way.

Here's how it looks in practice (using some sample data used to generate the initial mockups):

<img src="https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning.gif" alt="Individual Reckonings" style="max-width: 24%;"/>
<img src="https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning+\(Closed\).gif" alt="Individual Reckoning (Closed)" style="max-width: 24%;"/>
<img src="https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Front+Page+Logged+Out.gif" alt="Front Page: Anonymous" style="mmax-width: 24%;"/>
<img src="https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Profile+Main+Page.gif" alt="User Profile" style="max-width: 24%;"/>

There's some salty language in the sample data, but The Reckoner was designed as a civil, long-standing resource meant to provide honest, well-considered resolutions to even frivolous questions.  That's why the submitted questions are proctored, and real identities are required for commenters.

## Aha! But why?

This was built mostly as a way to decompress after six years in the Big Government and Commercial Consulting business, and to achieve three main goals:

1. To complete the always-satisfying process of defining and building a production-grade **product** from scratch.
2. As an opportunity to work with some technologies with which I wanted to build a production-grade system (MongoDB, Django 1.4, Amazon CloudFront CDN, etc.)
3. Most importantly: as a low-risk pretense to feel out the software start-up ecosystem in preparation for a more concerted effort over the next 2-3 years.
 
The Reckoner officially launched on November 30th, 2011.  Within four months, it had more than 250,000 pageviews from more than 65,000 unique visitors.  It ran precisely one year, and then I brought the site down having achieved each of the three goals I had set out for the project.

In April of 2012, I joined [Artisan Mobile](www.useartisan.com) as a Senior Architect, which is the next phase of the plan noted in (3) above.

## Cool.  What now?

Now I've open-sourced it.  The code is largely untouched from November of 2011, but much of this is still a great way to explore an applied example of Django, MongoDB, Spring Data, Facebook/Google OAUTH2, and other components in action.  All code, art assets, and everything else here was developed by yours truly (Daniel Koch), and is open-sourced as part of the GPLv3 license.

For the curious and intrepid, feel free to ask me any questions about how this works.  The Wiki for this code repo has a basic overview on how the different components work together and how to get a development environment set up.  All of this runs on AWS (as part of an auto-scaling group), and I'd be more than happy to offer a few pointers on how to get an instance of this spinning.

**Thanks, and cheers!**

Daniel Koch<br>
June 23, 2013
