# Fling
## Fling is a side project management platform.

Fling is a tool for those of us who cannot help but create new side projects - flings. Some flings are started late at night and forgotten about the next day, while others we may continue working on over many weekends. Some may generate income, while others drain our savings. With so many projects in some state of development, keeping track of your flings, your fling's social media accounts, user activity or even where they're hosted can be nothing short of a nightmare. This tool is meant to help with that.

Fling allows you to collect and store "business state" separate
from both the source code (which lives in a git repo), and app
state (which usually lives in a production database somewhere).

Business state is:

 - Hosting details (where is it running)
 - Socials (blog, insta, mastodon)
 - Monthly costs
 - Income (revenue or donations)
 - Basic user stats (views, signups, sessions)
 - Partnership details (who built it with you)
 - History / Timeline (when was it started, deployed etc)

It consists of a CLI tool, a web service, and a cookiecutter template.

The CLI, along with a growing set of plugins, can be used to gather
"business state" about your project, and store that in the Fling service.

The cookiecutter template is language agnostic, and can be used for any 
new side project. It will add a *company-private* web interface that
can be used to browse and visualize your side project state.

<INSERT single side project company view here>

The Fling web service can be authenticated with GitHub, and used to aggregate
the Fling business state from *all* of your side projects.

<INSERT aggregated view screenshot here>

## Fling CLI plugins

### Namer

The namer plugin can be used through the ```search``` command. It uses ChatGPT to 
come up with great domain name ideas, and then the Name.com API to find some that
are available.

### Init

The init plugin is integrated with cookiecutter, and can be used to set up a new
side project with Fling support. Existing projects can be configured by manually 
creating a ```fling.yaml``` file and then running ```fling pull```.