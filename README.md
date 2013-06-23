## The Reckoner, eh?

Yes, The Reckoner!  The Thunderdome for Decisions!

The Reckoner was a web application built in the Fall of 2011 that was founded on one elementary concept:

* Got a binary question?
* Good or bad?  
* Yes or no?  
* Happy Days better with Chachi or without Chachi? 
* **Submit it to the Reckoner and let the world decide!**
 
Yes, the core concept really was that simple. People submit questions with two possible answers, the questions get approved and spruced up, and posted on the site for a week.  At the end of the week, you have your answer.  This was always intended as a toy, but a *fun* toy, and sometimes fun toys have a way of ingratiating themselves into people's lives in a satisfying way.

Here's how it looks in practice (using some sample data used to generate the initial mockups):

[![Closed Reckonings List](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Closed+Reckonings+Screen+Thumbnail.gif)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Closed+Reckonings+Screen.gif)
[![Individual Reckonings](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning+Thumbnail.gif)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning.gif)
[![Individual Reckoning (Closed)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning+%28Closed%29+Thumbnail.gif)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Individual+Reckoning+%28Closed%29.gif)
[![Front Page: Anonymous](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Front+Page+Logged+Out+Thumbnail.gif)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Front+Page+Logged+Out.gif)
[![User Profile](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Profile+Main+Page+Thumbnail.gif)](https://s3.amazonaws.com/Working_Dan_Files/Reckoner+Mockups/Profile+Main+Page.gif)

There's some salty language in the sample data, but The Reckoner was designed as a civil, long-standing resource meant to provide honest, well-considered resolutions to even the most frivolous of questions.  That's why the submitted questions were proctored, and real identities required for commenters.  It was also built for maximum scalability, so the technical architecture is more involved than what would typically be associated with a standard CRUD webapp such as this.

## Aha! So why did you build it?

After six years in the Big Consulting business, I embarked on the Reckoner project as a means to achieve three goals:

1. To complete the always-satisfying process of defining and building a **product** from scratch.
2. As an opportunity to work with some technologies with which I wanted to build a production-grade system (MongoDB, Django 1.4, Amazon CloudFront CDN, etc.)
3. Most importantly: as a low-risk pretense to feel out the software start-up ecosystem in preparation for a more concerted effort over the next 2-3 years.
 
The Reckoner officially launched on November 30th, 2011.  Within four months, it had more than 250,000 pageviews from more than 65,000 unique visitors, including several hundred daily recurring users.  It ran precisely one year, and then I brought the site down having achieved each of the three goals initially defined for the project.

In April of 2012, I joined [Artisan Mobile](http://www.useartisan.com) as a Senior Architect, which is the next phase of the plan noted in (3) above.

## Cool.  What now?

Now I've open-sourced it.  The code is largely untouched from November of 2011, but much of this is still a great way to explore an applied example of Django, MongoDB, Spring Data, Facebook/Google OAUTH2, and other components in action.  All code, art assets, and everything else here was developed by me (Daniel Koch), and is open-sourced as part of the GPL v3 license.

For the curious and intrepid, feel free to ask me any questions about how this works.  The Wiki for this code repo has a basic overview on how the different components work together and how to get a development environment set up.  All of this runs on AWS (as part of an auto-scaling group), and I'd be more than happy to offer a few pointers on how to get an instance of this spinning.

**Thanks, and cheers!**

Daniel Koch<br>
June 23, 2013
