## I Am Using GitHub Under Protest

Please join the [conversation on dev.to](https://dev.to/pboling/im-leaving-github-50ba).

Github's decision to sponsor me is so recent that I haven't been able to cash out the $550 payment yet.

In spite of that, I can't leave the platform fast enough.  I certainly do not have the spare-time to move **hundreds** of projects to a new home... but I'm getting started.

GitHub is a proprietary, trade-secret system that is not Free and Open Souce Software (FOSS).  I am [deeply concerned](https://sfconservancy.org/blog/2022/jun/30/give-up-github-launch/) about using a proprietary system like GitHub to develop FOSS projects.

# Micro Issues

1. A recent proposal to extend Github-flavored Markdown ([ref](https://github.com/github-community/community/discussions/16925#discussioncomment-3095850))
    - Literally [breaks](https://github.com/github-community/community/discussions/16925#discussioncomment-3014438) regular markdown syntax of links in headings.
    - [English-only](https://github.com/github-community/community/discussions/16925#discussioncomment-3086634)
    - Incompatible with Semantic HTML (POSH) (by [abusing](https://github.com/github-community/community/discussions/16925#discussioncomment-2830438) the `blockquote` tag; this also raises issues of [accessibility](https://github.com/github-community/community/discussions/16925#discussioncomment-3095850))
    - Incompatible with existing [Markdown standards proposals](https://github.com/github-community/community/discussions/16925#discussioncomment-2791869)
    - Rudely ignorant of the community-centered approach to [extending Markdown](https://github.com/github-community/community/discussions/16925#discussioncomment-3095850), which, ironically, [Github started](https://github.com/github-community/community/discussions/16925#discussioncomment-3101018)
    - [Contributes](https://github.com/github-community/community/discussions/16925#discussioncomment-2975948) to vendor [lock-in](https://github.com/github-community/community/discussions/16925#discussioncomment-2806570).
    - Will force countless volunteer FOSS developers to waste time [adding compatibility](https://github.com/github-community/community/discussions/16925#discussioncomment-3086904) to their projects that use Markdown and attempt to support GFM.
2. More than 2 years of ignoring requests to add an important feature (`allow-failure`) to Github Actions ([ref](https://github.com/actions/toolkit/issues/399), [ref](https://github.com/github-community/community/discussions/15452)).  When not ignoring, Github is [completely misunderstanding](https://github.com/actions/toolkit/issues/399#issuecomment-607450398) the feature.  How are those building Github Actions so deeply **unfamiliar** with core features of competing CI platforms.
3. Latest iteration of [Achievements](https://github.com/github-community/community/discussions/18153#discussioncomment-2935669) was bad.
4. Microsoft (parent of Github) has decided to [ban commercial open source](https://sfconservancy.org/blog/2022/jul/07/microsoft-bans-commerical-open-source-in-app-store/) apps from their app store.

---

# Macro Issues

For a broad perspective on the practical issues, I can't make the argument any better than it [was in 2010](https://forgefriends.org/blog/2022/06/30/2022-06-state-forge-federation/), and for me this issue has crossed the Rubicon, and recently by [Software Freedom Conservancy](https://sfconservancy.org/), [here](https://sfconservancy.org/blog/2022/jun/30/give-up-github-launch/) and [here](https://sfconservancy.org/GiveUpGitHub/).

<figure>
  <a href="https://sfconservancy.org/GiveUpGitHub/"><img align="left" width="50%" src="https://sfconservancy.org/img/GiveUpGitHub.png" alt="Logo of the GiveUpGitHub campaign"></a>
  <figcaption>For those who've never heard of the <a href="https://sfconservancy.org/GiveUpGitHub/">Software Freedom Conservancy</a>, <a href="https://sfconservancy.org/projects/current/">member projects</a> include: <a href="https://backdropcms.org/">Backdrop CMS</a>, <a href="https://www.coreboot.org/">Coreboot</a>, <a href="http://darcs.net/">Darcs</a>, <a href="https://git-scm.com/">git</a> (yes, <em>the</em> git in Github), <a href="https://inkscape.org/">Inkscape</a>, <a href="https://microblocks.fun/">MicroBlocks</a>, <a href="https://www.mercurial-scm.org/">Mercurial</a>, <a href="https://openwrt.org/">OpenWRT</a>, <a href="https://phpmyadmin.net/">phpMyAdmin</a>, <a href="http://qemu.org/">QEMU</a>, <a href="https://www.samba.org/samba/">Samba</a>, <a href="http://seleniumhq.org/">Selenium</a>, <a href="http://squeak.org/">Squeak</a> and <a href="http://www.winehq.org/">Wine</a>, among others.
  </figcaption>
</figure>

## What about community?

I am interested in people's thoughts on where to go next.  Community involvement matters for open source projects, and I have dozens of them that could be affected, the biggest being [`oauth`](https://rubygems.org/gems/oauth) and [`oauth2`](https://rubygems.org/gems/oauth2) Ruby gems.

Regarding fragmentation, hopefully it will be resolved by federation, which is to source forges (like Github) what git was to version control (i.e. makes it distributed, at least in theory).

It looks like Gitea, Codeberg and Hostea will [join the fediverse](https://forgefriends.org/blog/2022/06/30/2022-06-state-forge-federation/) soon, within a year, and there are projects that will integrate Github with the fediverse as well (i.e. federate Github commits, PRs, issues, etc).

## Questions

- Have any major Ruby projects already left?
- Anyone have experience with mirroring to multiple git hosts, as that might be a temp bridge solution?
- Self-hosting a git service?
- Thoughts on the centralized git hosting providers recommended by SF Conservancy?

## Poll

*Where to take projects (e.g `oauth2`)?*

- https://github.com/oauth-xx/oauth2/discussions/622

### :wave: Hi there

<div id="badges">

  [![Follow Me on Twitter](https://img.shields.io/badge/PeterBoling-blue?style=plastic&logo=linkedin)](http://www.linkedin.com/in/peterboling)
  [![Follow Me on LinkedIn](https://img.shields.io/twitter/follow/galtzo.svg?style=social&label=Follow)](http://twitter.com/intent/user?screen_name=galtzo)
  [![Published Rubygems](https://img.shields.io/gem/u/pboling.svg)](https://rubygems.org/profiles/pboling)
  [![Github Profile Views Since 2022.02.13](https://komarev.com/ghpvc/?username=pboling)](https://komarev.com/ghpvc/?username=pboling)

</div>

# Blog posts
<!-- BLOG-POST-LIST:START -->
- [I&#39;m leaving Github](https://dev.to/pboling/im-leaving-github-50ba)
- [I use shared hosting as my build server. Here&#39;s how.](https://dev.to/pboling/i-use-shared-hosting-as-my-build-server-heres-how-2e6k)
- [Matrix: Ruby, Gem, Bundler, etc](https://dev.to/pboling/matrix-ruby-gem-bundler-etc-4kk7)
- [Rubocop LTS](https://dev.to/pboling/rubocop-lts-1e31)
- [Rubocop... but SemVer](https://dev.to/pboling/rubocop-ruby-matrix-gems-nj)
<!-- BLOG-POST-LIST:END -->

# Contributions

![GitHub Snake Light](https://github.com/pboling/pboling/raw/output/github-snake.svg?raw=true#gh-light-mode-only)
![GitHub Snake dark](https://github.com/pboling/pboling/raw/output/github-snake-dark.svg?raw=true#gh-dark-mode-only)
![Comment Reactions](https://github.com/pboling/pboling/raw/main/dist/metrics.plugin.reactions.svg?raw=true)
![Notable Contributions](https://github.com/pboling/pboling/raw/main/dist/metrics.plugin.notable.svg?raw=true)

## :child: How it started...

<figure>
  <img align="left" width="25%" src="https://railsbling.com/peter-amazon-black-caiman.jpg" alt="Holding a black caiman, Amazon River, Brazil. 1997">
  <figcaption>A cheeky me holding a baby black caiman, Amazon River, Brazil, June 24, 1997, shortly after completing my first programming course - Pascal. The <a href="https://en.wikipedia.org/wiki/Black_caiman">black caiman</a>, a baby specimen of the family Alligatoridae and order Crocodilia, was unharmed, and released back to the water, where it promptly continued following its mother. Full grown they are among the largest alligators and crocodiles in the world<a src="https://github.com/ElectricRCAircraftGuy/eRCaGuy_hello_world/blob/master/markdown/github_readme_center_and_align_images.md">.</a></figcaption>
</figure>

## :godmode: How it's going...

- 🦷 I'm putting more of my focus on FLOSS efforts (of myself and others)! <img src="https://img.shields.io/liberapay/gives/pboling.svg?logo=liberapay"> and <img src="https://img.shields.io/liberapay/receives/pboling.svg?logo=liberapay"> from <img src="https://img.shields.io/liberapay/patrons/pboling.svg?logo=liberapay">
- 👷 I build big things and small things out of tiny bits.
- ✨ Recently created [`rubocop-lts`](https://github.com/rubocop-lts) for library maintainer happiness 👩‍❤️‍👩.
- 🔭 I’m working on switching my gem libraries to use Github Actions for CI
- 🌱 I’m learning Svelte, and I want to learn Rust next
- 👯 Preparing transition to v2 of the `oauth2` gem!
- 🤔 I’m looking for help with maintaining my suite of Resque plugins, as I don't have a current use case for Resque.
- 📫 How to [reach me](https://about.me/peter.boling)
- 😄 Pronouns: He/Him
- 🗨️ I speak 3 languages fluently, and for a 4th I'm learning Bahasa Indonesia!
- 👷‍♂️ I help refugees and ex-refugees in Ghana🇬🇭 and Liberia🇱🇷, respectively, through Hope For Tomorrow, a Liberian NGO.  DM me if interested in knowing more.

[next-milestone-pct]: https://github.com/oauth-xx/oauth2/milestone/1
[next-milestone-pct-img]: https://img.shields.io/github/milestones/progress-percent/oauth-xx/oauth2/1

<details>
  <summary>:hammer_and_wrench: My Dev Tools:</summary>
  <div id="tools">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original.svg"
       alt="AWS" title="AWS" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-plain.svg"
       alt="bash" title="bash" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/circleci/circleci-plain.svg"
       alt="circleci" title="circleci" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/codecov/codecov-plain.svg"
       alt="codecov" title="codecov" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-plain.svg"
       alt="css3" title="css3" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/debian/debian-plain.svg"
       alt="debian" title="debian" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/digitalocean/digitalocean-original.svg"
       alt="digitalocean" title="digitalocean" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-plain.svg"
       alt="docker" title="docker" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-plain.svg"
       alt="git" title="git" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg"
       alt="github" title="github" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/gitlab/gitlab-plain.svg"
       alt="gitlab" title="gitlab" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/gitter/gitter-plain.svg"
       alt="gitter" title="gitter" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/graphql/graphql-plain.svg"
       alt="graphql" title="graphql" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/handlebars/handlebars-original.svg"
       alt="handlebars" title="handlebars" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/heroku/heroku-plain.svg"
       alt="heroku" title="heroku" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jamstack/jamstack-original.svg"
       alt="jamstack" title="jamstack" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-plain.svg"
       alt="javascript" title="javascript" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jetbrains/jetbrains-original.svg"
       alt="jetbrains" title="jetbrains" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jira/jira-plain.svg"
       alt="jira" title="jira" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/kubernetes/kubernetes-plain.svg"
       alt="kubernetes" title="kubernetes" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-plain.svg"
       alt="linux" title="linux" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/markdown/markdown-original.svg"
       alt="markdown" title="markdown" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-plain.svg"
       alt="mysql" title="mysql" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/neo4j/neo4j-plain.svg"
       alt="neo4j" title="neo4j" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-plain.svg"
       alt="nodejs" title="nodejs" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-plain.svg"
       alt="postgresql" title="postgresql" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/rails/rails-plain.svg"
       alt="rails" title="rails" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/ruby/ruby-plain.svg"
       alt="ruby" title="ruby" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/rubymine/rubymine-plain.svg"
       alt="rubymine" title="rubymine" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/svelte/svelte-plain.svg"
       alt="svelte" title="svelte" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/wordpress/wordpress-plain.svg"
       alt="wordpress" title="wordpress" width="28" height="28" />
  </div>
</details>

## :briefcase: Career

- The list is long, even in summary, see [my LinkedIn](https://www.linkedin.com/in/peterboling/).

### :roll_of_paper: Current Roles

- Staff Software Engineer | [Underdog Sports](https://underdogfantasy.com)
- Outreach, Tech, Comms | [#UnitedLeft (on Discord)](https://discord.gg/3yhwAr7)
- Advisor | [Hope For Tomorrow (Liberian NGO)](https://www.facebook.com/hope.for.tomorrow.liberia)
- FOSS Blogger | [RailsBling](https://railsbling.com)
- FOSS Author | [RubyGems](https://rubygems.org/profiles/pboling)
- Researcher | [WordTree Foundation](http://wordtree.org/)
- Member-worker | [Bed of Roses Club](http://bed-of-roses.club/)

[![Open Hub profile](https://www.openhub.net/accounts/peterboling/widgets/account_detailed?format=gif&amp;ref=sample)](https://www.openhub.net/accounts/peterboling?ref=sample)

<a href="https://github.com/anuraghazra/github-readme-stats#github-stats-card">
  <img align="center" src="https://github-readme-stats.vercel.app/api?username=pboling&count_private=true&show_icons=true&theme=tokyonight" />
</a>
<a href="https://github.com/anuraghazra/github-readme-stats#top-languages-card">
  <img align="center" src="https://github-readme-stats.vercel.app/api/top-langs/?username=pboling&theme=tokyonight&layout=compact&hide=rich%20text%20format" />
</a>
