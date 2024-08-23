# Function Block Environment

An application for modelling function blocks based on IEC 61499. 

## Requirements:
 - Python3
 - GNOME Builder (Available only for LINUX)
 - Flatpak (Required for installing GNOME Builder)
    
### How to install Builder:
 1. Install Flatpak:
    ```
    sudo apt install flatpak
    ```
 3. Add the flathub repository:
    ```
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    ```
 4. Restart your system
 5. Install GNOME Builder:
    ```
    flatpak install flathub org.gnome.Builder
    ```

## To run FBE:
 1. Clone the FBE repository:
    ```
    git clone https://github.com/cabralbonin/fbe3_gnome.git
    ```
 3. Open Builder then add the FBE project.
 4. Open the project
 5. Run project (Shift+Ctrl+Space)

## How to use:
#### When no project is open, this is what the application looks like:
!["No project open."](https://github.com/user-attachments/assets/063bae90-5ae6-4098-8046-632c894e5f50)

#### On the left side there's the editor workspace with basic tools like add, move, inspect, delete and connect. 
![editorworkspace](https://github.com/user-attachments/assets/ba16acda-1554-4ab0-b3c4-74049b2f5d5c)

#### Right below there's the import library space, where you can load a library (e.g., home/user/documents/mylibrary) and also refresh once there's a change in the directory.
![loadlibrary](https://github.com/user-attachments/assets/04dc3313-73e9-4332-a20b-f762cf60ae1f) 
![loadinglibrary](https://github.com/user-attachments/assets/5c9c80bc-5cfe-4c0c-a33c-1596eb74d66d)
![loaledlibrary](https://github.com/user-attachments/assets/9ed03a2f-88ba-48f1-accb-fc3918b41ae2)
#### When adding a element to the project, remember to load a library (if the element has nested elements) to properly work.

#### The header bar also holds some important functions:
![headerbar](https://github.com/user-attachments/assets/c9778672-4c1f-4199-93f0-c160ca552779)

#### The left button presents the options to create, open, save, save as and export a project
## IMAGE
#### While the right button is where you can access preferences, keyboard shortcuts, read about FBE and also quit the application 
## IMAGE


#### Upon creating a new project, it creates a blank unnamed system (which can refered as project) and application. The main page of every project it's the System Information. Through this page is possible to access every element of the project the user whishes to inspect by double clicking at element.
![accesselementdouble](https://github.com/user-attachments/assets/28aff462-35e5-478d-88c7-76f85f3e0805)
![image](https://github.com/user-attachments/assets/72f2c940-6569-42c8-806b-093317cc23ad)

#### Most pages can be accessed by shortcuts, here's the most useful ones:
- System Information `Ctrl+G`
- System Configuration `Ctrl+H`
- Go to next application `Ctrl+D`
- Go to previous application `Ctrl+A`
- Go to last accessed page `Ctrl+B`
- Add type to application `Ctrl+Alt+N`
- Export project `Ctrl+E`

#### Elements with inside elements (e.g., Composite FB, FB's ECC, Device's FB Network) can be accessed by using the inspect tool and clicking on the element.
![inspect](https://github.com/user-attachments/assets/1d17a924-6960-4327-bf60-186cdcf0d16d)
![image](https://github.com/user-attachments/assets/6e4f72ff-a5fa-42c5-a34e-7c2f164ffb68)

#### The whole project or part of it can be exported through the export page(Ctrl+E):
![image](https://github.com/user-attachments/assets/979f62e8-1759-4cc2-af8c-70cfce70df18)

