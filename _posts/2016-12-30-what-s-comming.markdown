---
layout: post
title:  "A more usable condor ir"
date:   2016-12-30 19:53:23
categories: announcement
---

In 2016 the development of `condor-ir` was a bit slow, after a fast period
towards the start of the year life happened and the project got a little bit
delayed.

Nevertheless, we got some nice features in, we got nice extraction of bibtex,
isi and froac file-formats, a complete database schema for bibliographic
information and a nice CLI that allows us to work with bibliography sets, term
document matrices and search engines.

We also jumped from mongo db, a nice but not as scalable solution for data
storage, to a strict postgresql schema. This data storage promise to be more
scalable and error resilient, plus, it might allow for faster queries.

The CLI is nice, however it might get cumbersome for not console heavy people
(I as a developer spend my whole day in the terminal, even refusing to use an
graphical ide) for that reason one of the next steps will be to build a nice
and safe `grapql` API so that we can build graphical user interfaces on top of
that.

I expect to spend some time then to build a client for `condor-ir`, the primary
features might be:

- Term document matrix and search engine management.
- Bibliography set aggregation.
- Support to manage contributor information.

Off course, I wouldn't like to deal with big files at the moment, that's why
bibliography set loading (specially with full text detection) will have to
wait.

Remember that contributions are open and you can communicate with the
maintainers for information retrieval training and discussion.
