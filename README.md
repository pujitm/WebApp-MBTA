# WebApp-MBTA

This is the base repo for MBTA project. Please read [instructions](instructions.md).

notes on mbta api usage/instructions

my first instinct was that making an api call everytime we want to find the nearest station is way overkill because stations dont change all that often.
then i ran the `stops` endpoint and got a 10mb response in return, which upset me cuz thats poor design.

It's way better to do some data pre-processing to make things efficient.

- hence the static json files
- more memory on server is cheaper than bandwidth (in most cases)

## Part 2

`FLASK_APP=mbta flask run`

## Part 3: Reflection

Web app to find the nearest MBTA station to a named location.

Process: Fortunately, very little of my code needed to be changed from pt1 to pt2.

The most important implementation choices were caching the MBTA stop information and the data structure to query when searching for the nearest station.
Caching was a pretty obvious choice, as written above, but I was considering a couple of other choices. A tree is the basic progression past brute force, so I used it because it was convenient, and further optimization is overkill. It gets us to logarithmic complexity instead of linear complexity, and that's what's important.

We trade memory/disk space/startup-time for less bandwidth usage, which will be more expensive at smaller scales, but the application will always be highly responsive.
