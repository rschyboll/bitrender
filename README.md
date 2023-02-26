<br />
<div align="center">
  <h3 align="center">BITRENDER</h3>
  <p align="center">
    A Render farm software for Blender.
  </p>
</div>

> :warning: **DISCLAIMER**: If you're looking for reliable render farm software, I recommend checking out options like <a href="https://www.crowd-render.com/">Crowdrender</a> or other solutions that are already established and ready for use. While I appreciate your interest in Bitrender, I cannot guarantee its readiness as it's mainly a learning sandbox for me.

## About The Project

There are already many services available that allow for the distribution of animation rendering from Blender, with <a href="https://www.crowd-render.com/">Crowdrender</a> being one of the most popular options. However, one thing that has always bothered me is whether it's possible to distribute one frame across multiple machines. As it turns out, it is possible, and Crowdrender already does this quite well.

However, there was one idea that still drove me to create this project: is it possible to split a frame not by tile splitting, but by rendering the entire image on different machines with different sample offsets? This feature was recently added to Blender, and i needed a project for my Engineering Thesis. That's how Bitrender came to be.

## What sets Bitrender apart from other software options?
The big difference with Bitrender is its splitting algorithm. Without going into too much detail, this algorithm allows for a frame to be split in such a way that each machine completes the render simultaneously and in a known amount of time. 

It achieves this by first assessing the performance of each machine, and then creating a short render for a specified amount of time (e.g. one minute). If it finishes, the frame is used as the result. If not, it takes the frame, checks how many samples were rendered, and then uses this data to split the remaining samples between other machines so that the render times are the same on each of them.

Is this the most efficient or best way to split frames for rendering? Probably not. It was simply an idea that I liked and it seems to work.

## Potential future plans? 
Currently, not really. I worked on this project while also working a full-time job as a software developer, and I need to take a break from it for the time being.

If I do return to working on Bitrender, there are a few things I might change:
* Add a Blender plugin. Sending projects through a website is tedious, and a plugin would be a quality-of-life improvement.
* Finish implementing user management. I started it, but it still has a long way to go.
* Maybe change the tech stack? Using libraries like FastAPI was fun and I learned a lot, but libraries like Django have already working user management. So, I might choose a library with more features out of the box.
* To be honest, I might just use <a href="https://www.crowd-render.com/">Crowdrender</a>. It's probably not worth reinventing the wheel 🙃."


### How to use
Unfortunately, there is currently no easy way to use Bitrender. 

While it's possible to launch both the frontend and backend through Docker and the Devcontainer extension from VSCode, the current branch does not include any code for managing a render farm. 

The code for splitting frames and managing a render farm is buried deep within the commits, but I plan to dig it up in the future and create a Docker configuration that would allow for its launch.

<!-- CONTACT -->
## Contact
Email: robin.schyboll@gmail.com
