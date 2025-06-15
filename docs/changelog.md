[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 5.3.0

- Refactored the code for better maintainability.
  Reintegrated the controller mixin class into the view class.
- Reformatted parts of the code according to PEP-8.

API: 5.0
Based on novelibre 5.26.4


### Version 5.2.5

- Disabling the toolbar button when closing the project.

API: 5.0
Based on novelibre 5.16.3


### Version 5.2.4

- Refactored the code for better maintainability.

API: 5.0
Based on novelibre 5.16.2


### Version 5.2.3

- Making the resizing of the window smoother on low-end systems.

API: 5.0
Based on novelibre 5.11.0


### Version 5.2.2

- Set the minimum window size to 400x400 (#1). This fixes a bug where an exception is raised when the window is made too narrow.
- Refactored the code for better performance.
- Changed the section default color from "coral1" to "greenyellow". 
  To make this take effect, you may want to delete `statistics.ini` in the `.novx/config` directory. 

API: 5.0
Based on novelibre 5.11.0


### Version 5.2.1

- Handling zero division error in case there are no words. 

API: 5.0
Based on novelibre 5.6.0


### Version 5.2.0

- Added a toolbar button.
- Refactored for more efficiency. 

API: 5.0
Based on novelibre 5.6.0


### Version 5.1.1

- Secured the calculation against overflow. 

API: 5.0
Based on novelibre 5.6.0


### Version 5.1.0

- Show the section positions in the viewpoint tab.
- Show the section positions in the plot lines tab.


### Version 5.0.0

- Rewritten using tk.canvas display.
- Added scrollbars.
- Activated mouse scrolling.
- Placing parts, chapters, sections, and stages sequentially. 

Library update:
- Refactor the code for better maintainability.

API: 5.0
Based on novelibre 5.0.28

### Version 0.2.4

Refactor for better maintainability:

- Make the Plugin constructor extend the superclass constructor.

Based on apptk 2.2.0

### Version 0.2.3

- Provide localized help link.

Based on apptk 1.1.0
Compatibility: novelibre version 4.11 API

### Version 0.2.2

- Update the help link.

Based on apptk 1.1.0
Compatibility: novelibre version 4.11 API

### Version 0.2.1

- Fix help page.
- Change the window title.
- Refactor.

Based on apptk 1.1.0
Compatibility: novelibre version 4.11 API

### Version 0.2.0

- Select tree elements on double-click.

Based on apptk 1.1.0
Compatibility: novelibre version 4.11 API

### Version 0.1.0

- Alpha release under the GPLv3 license.

TODO:
- Enable vertical scrolling.
- Keep the "Close" button when shrinking the window. 

Based on apptk 1.1.0
Compatibility: novelibre version 4.11 API
