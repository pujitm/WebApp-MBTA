# WebApp-MBTA

This is the base repo for MBTA project. Please read [instructions](instructions.md).

notes on mbta api usage

my first instinct was that making an api call everytime we want to find the nearest station is way overkill because stations dont change all that often.
then i ran the stops endpoint and got a 10mb response in return, which pissed me off cuz thats poor design
it's way better to do some data pre-processing to make things efficient.

hence the static json files
more memory on server is cheaper than bandwidth (in most cases)

## Part 2

`FLASK_APP=mbta flask run`
