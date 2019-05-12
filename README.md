<h1> Farmbot Techlauncher </h1>

<h2><a name = "content"> Table of Contents </a></h2>
<a href = "#Title1"><b> 1. Project Description </b></a><br/>
<a href = "#Title2"><b> 2. Project Administration </b></a><br/>
<a href = "#Title3"><b> 3. Documentation </b></a><br/> 
<a href = "#Title4"><b> 4. UML Diagram </b></a><br/>
<a href = "#Title5"><b> 5. Current Progress </b></a><br/>
<a href = "#Title6"><b> 6. Technical Tools and Constraints </b></a><br/>


<br />
<h2><a name = "Title1"> 1. Project Overview </a></h2>

[Farmbot](https://farm.bot/) is an autonomous agricultural tool which works over a small area to test small-scale agriculture, and has the potential to eventually become a framework for driverless tractors or drones. Current Farmbot software has the capability for simple placement of individual plants, and execute simple commands like watering and fertilizing certain plants. Our expectations of the project is to adopt machine learning skills and modelling techniques to reinforce the capability of Farmbot to automate group plantations and duplicate commands. Our modifications on Farmbot aim to enhance the capability of controlling and monitoring. Our priorities are to optimise plant management and leverage the technology of the Farmbot platform.

<br />
<h2><a name = "Title2"> 2. Project Administration </a></h2>

<h3> 2.1 Timeline </h3>

Week 2-3 Discovery Stage <br />
Week 4-5 Alpha Version - Able to send commands to Farmbot <br />
Week 6-9 Beta Version - Most commands have been implemented in code, which compiles and is received by Farmbot. Data is able to be input  through CSV or text files <br />
Week 10-12 Reflection and Improvements <br />

<h3> 2.2 Deliverables </h3>

* Modular Python code that implements:
    * New version of Farm Design, which accepts CSV files as a way of defining groups of plants, and also keeps some of the original functionality such as telling you when plants are too closely spaced together, and displaying information on the plants.
    * New version of the existing sequences, which are associated with Farm Design groups, supports loops, accepts JSON, yaml, or text files as ways of defining these tasks, and has the option to output logs in both CSV and custom text format
    * New text-based implementation of Regimens, which are associated with Farm Design groups.
    * New text-based implementation of Farm Events, which are associated with Farm Design groups.
    * Some way to test commands without ruining the garden bed.
    * All implementations should also be able to create, edit and write to files that store these Farm Designs, Sequences, Regimens, and Events, and have their callable functions structured in a way that would easily support the future addition of a GUI.
    
* Documentation:
    * High level documentation of the code, to be done as we go in a wiki format on GitHub
    * Well commented code
    * Commit messages should be a good description of changes made in that commit. If you want to make many changes, please do it in separate commits.
    * A guide on how to use the resulting code, to be handed to the stakeholders and made available on GitHub

<h3> 2.3 Traceability of Actions </h3>



>[Decision Log](https://docs.google.com/document/d/1AfgSXgv-pHwiSv7r8mqHihJIXiVt2jJx9cPXHvMyFtYedit?usp=sharing) <br />

<h3> 2.4 Team </h3>

| Team Member                      | Role                                     | Email                           | 
|----------------------------------|------------------------------------------|---------------------------------|  
| Patrick Benter                   | Team Leader, DevOps, Programmer          | u5583834@anu.edu.au             |
| Zhixian Wu                       | Delivery Manager, Programmer             | u5807060@anu.edu.au             | 
| Maojun Zhu                       | Team Coordinator, Programmer             | u6170753@anu.edu.au             |
| Zizheng Huang                    | Programmer                               | u6248330@anu.edu.au             |
| Yutian Wang                      | Programmer                               | u6269498@anu.edu.au             |
| Wei Ren                          | Programmer                               | u6233682@anu.edu.au             |
| Wenjing Gu                       | Project Manager, Programmer              | u6203160@anu.edu.au             |

<h3> 2.5 Stakeholders </h3>

* Client: Ming-Dao Chia. 
    * Communication Method: Slack and weekly meetings 
    * Ming has found the current FarmBot interface cumbersome and wants a more powerful one. He is not developing the software but he and his will be using it regularly. This is a strong motivation to write a clear, accessible user guide.
    * High Interest, High Power
* Hardware Team
    * There is a hardware team designing new tools for the FarmBot. Most of our work is separate from theirs, but if they finish any tools early we may have time to connect it to the FarmBot software with CeleryScript.
    * Medium Interest, Medium Power
* Tutors and Program Conveners:
    * We are being assessed on our work by our tutor and program conveners.
    * High Interest, High Power
* All current users of FarmBot 
    * FarmBots are produced by a company which ships them worldwide. They are used in multiple continents for research, teaching, and other purposes. The current FarmBot software is open-source under an MIT license and the code we produce will also be open-source and free for all current users of FarmBot to use and expand on, e.g. to add a GUI. 
    * This is another motivation to write an accessible user guide.
    * Low to Medium Interest, Low Power.

<br />
<h2><a name = "Title3"> 3. Support Documentation </a></h2>

>[Google Drive](https://drive.google.com/drive/folders/16XlRWSlGrqiolu_-3hwJq_npcvXVY4Z9?usp=sharing)

**Statement of Work**

>[Statement of Work](https://docs.google.com/document/d/1FSB61TqXdBAb-pXFtHVFb-pJZitc8AbANnnLSZ1RSLc/edit?usp=sharing) <br />

**Team Communication**

>[Slack](https://anuappffarmbot.slack.com/messages/CGHMVT15J/) <br />
>[Meeting Minutes](https://drive.google.com/drive/u/0/folders/1jJi34sRYmjUgE1syTGPG4aYzWS5fJ-hc) <br />

**Team Progress Tracking**

>[Github issues](https://github.com/dopfer/Farmbot-Techlauncher/issues)<br />
>[Weekly Log](https://docs.google.com/spreadsheets/d/1Wc2fRnvIfTPPWfBzSRZM2Uqh6Ayl5jGhBfXq_vXEDsE/edit?usp=sharing) <br />
>[Gantt Chart](https://docs.google.com/spreadsheets/d/1jeA3NB04pLH-Al9xu7jpajUeytPWd9bDBCCzlKktllg/edit?usp=sharing) <br />

**Legal Documents**

Not required

<br />
<h2><a name = "Title4"> 4. UML Diagram </a></h2>
<img src="https://user-images.githubusercontent.com/26053128/55402300-dcda5280-559e-11e9-8ad8-fd12aee13a68.png" />
<br />

<h2><a name = "Title5"> 5. Current Progress </a></h2>

Current Progress: Able to send simple commands to the farmbot using program and see response

**Milestones:**

Phase 1: ~~Create a Discovery Report to demonstrate project specifications and requirements~~ <br/>
Phase 2: ~~Release an alpha version of the software, able to send simple commands to the Farmbot, replicating current functionality~~ <br/>
Phase 3: Release a beta version of the software, implementing most desired commands while integrating external input through text and CSV <br/>
Phase 4: Finalizing beta version and demonstrating functionality, developing handover documentation <br/>

<br />
<h2><a name = "Title6"> 6. Technical Tools and Constraints</a></h2>

* Available Tools:
    * One FarmBot XL for testing
    * Existing code base, particularly the RESTful API, which means it can work with modules written in other languages (originally written in Ruby)
* Constraints:
    * Some testing has to be done on site with physical machines
    * Python is the preferred language
    

