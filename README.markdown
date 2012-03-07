# Django Sandbox#

Site up at http://djangosandbox.alwaysdata.net 

Implemented **OpenID** for logging in. Library used: https://bitbucket.org/benoitc/django-authopenid

Implemented **Twitter-Bootstrap** : https://github.com/twitter/bootstrap/

The purpose of this site was just to learn web-dev with Django and Python from *Development to Deployment*. PyDev for Eclipse was used.

**Description:**

* This simple, **Profiles oriented**, Django powered website implements basic website tools such as Login and Register along with certain privileges to users.
* The privileges are such that it allows an authorized user to Edit their own profile details, change their login password. Every user is also allowed to view other user's profile.
* Unauthorized users do not have any privileges apart from viewing other profiles.
* Viewing other profiles will not allow editing or changing passwords. Authorized users can only view the details, logout or choose to go back to own profile.
I learnt how to grant and deny custom defined privileges to authorized and unauthorized users by implementing this.
* Apart from this, I implemented some customized form validation in the *Registration Form* page.
* The purpose of hosting it up on a free hosting was to understand how a website is finally deployed. I often notice that this phase of web-dev is ignored. But I wanted to understand this final step practically, and that's why I had it hosted. I must say that alwaysdata.net was very helpful, providing support individually wherever problems cropped up. It's also one of the few free web hosting sites that support Django.

Currently I'm trying to **implement the login feature using O-Auth for Google and Facebook**. 
