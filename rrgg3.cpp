#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <cstdlib>
#include <vector>
#include <sstream>
#include <fstream>

using namespace std;

vector <string> allStreetCommands(0);
vector <string> removeStreetNames(0);
vector <string> generatedCoords(0);


int randomNos(int k ,int min){
    int ktemp = k-min;

    std::ifstream urandom("/dev/urandom");
    if(urandom.fail()){
	std::cerr << "Error: cannot open /dev/urandom \n";
	return 1;
    }

    unsigned int num = 42;
    urandom.read((char*) &num, sizeof(int));

    int range = num % ktemp + min;
    urandom.close();
    return range;
}

string makeRandomCoord(int xcoord, int ycoord,  int k3, int k3b){
    string coord = "";
    xcoord = randomNos(k3 , k3b);
    ycoord = randomNos(k3 , k3b);

    string stringXCoord;
    ostringstream convertx;
    convertx << xcoord;
    stringXCoord = convertx.str();

    string stringYCoord;
    ostringstream converty;
    converty << ycoord;
    stringYCoord = converty.str();

          // cout << "( " << xcoord << " , " << ycoord << ")" << endl;
    coord = "(" + stringXCoord + "," + stringYCoord + ")";

    return coord;
}

string makeRandomName(){
    string name = "";
    for (int i = 0; i < 20; i++){
            int tempLetterNumber = randomNos(122, 97);

            char tempLetter = tempLetterNumber;

            name += tempLetter;
    }
    return name;
}

 void creatingStreets(int k1,int k2,int k3) {
     int streets, streetCount =0 , segments, coordCount = 0, attempts=0 ;
     int xcoord , ycoord , k3b = -k3;
     streets = randomNos(k1 , 2);
     // cout << endl;
     //cout << "Random no of streets = "  << streets << endl;
     allStreetCommands.empty();
     removeStreetNames.empty();
     generatedCoords.empty();



     while (streetCount++ < streets){
        string pythonAddCommand = "a \"";
        string streetName = makeRandomName();

        string pythonRemoveCommand = "r \"";
        pythonRemoveCommand = pythonRemoveCommand.append(streetName);
        pythonRemoveCommand = pythonRemoveCommand.append("\"");  // takes a generated street name, and converts it into r "streetname"

        removeStreetNames.push_back(pythonRemoveCommand);



        pythonAddCommand.append(streetName); // a "sdfsdafdsdasf"
        pythonAddCommand.append("\" ");
        string cordinates = "";

        segments = randomNos(k2,1);  // It will give random number of segments
        // cout << "Random no of segments = " << segments << endl;
        coordCount =-1;
        attempts =0;
        string indivStreetCoord = "";

     while(attempts++ < 25) {
         string coord = makeRandomCoord(xcoord, ycoord, k3, k3b);

       //check for the validity of x,y coordinates
       bool validCoord = true;

       for (int i = 0; i < generatedCoords.size(); i++){
        if (coord == generatedCoords[i]){
            validCoord = false;
        }
       }
       if (validCoord == true){
           generatedCoords.push_back(coord);
           coordCount++;
            if(coordCount <= segments) {

            indivStreetCoord = indivStreetCoord.append(coord);
            }
            else
                break;
       }

      if(attempts == 25){
        // generate r command for Assignment 1 for removing all streets
        cerr << "Error: failed to generate valid input for 25 simultaneous attempts" << endl;
        break;
      }   //end if(attempts == 25)
    } // end while(++attempts < 26)
    pythonAddCommand = pythonAddCommand.append(indivStreetCoord);
    // cout << pythonAddCommand << endl;
    allStreetCommands.push_back(pythonAddCommand);
 }   //end  while (streetCount++ < streets)
}


int main(int argc, char **argv)
{
    std::string svalue, nvalue, lvalue, cvalue;
     int k1 ,k2 , delay_value, k3, c, location;
    bool nflag = 0;
    location = 2;

    // cout << argc << endl;
    //for (int i=0; i< argc; i++){
    //    cout << "argv[" << i << "] = " << argv[i] << endl;
    //}
    while((c = getopt(argc, argv, "snlc")) != -1)
        switch(c) {
            case 's':
                svalue = argv[location];
                if(svalue.at(0) == '-') {
                   k1 = 10;
                   //cout << "Default number of streets = " << k1 << endl;
                   // call urandom()
                   location++;
                    break;
                }
                k1 = atoi(svalue.c_str());
                // std::cout << "Given number of streets = " << k1 << std::endl;
                location = location +2;
                break;
            case 'n':
                nvalue = argv[location];
                if(nvalue.at(0) == '-') {
                   k2 = 5;
                   // cout << "Default number of line segments = " << k2 << endl;
                   location++;
                    break;
                }
                k2 = atoi(nvalue.c_str());
                // std::cout << "Given number of line segments = " << k2 << std::endl;
                location = location +2;
                break;
             case 'l':
                 lvalue = argv[location];
                 if(lvalue.at(0) == '-') {
                   delay_value = 5;
                   // cout << "Default process wait time  = " << delay_value << endl;
                   location++;
                    break;
                }
                delay_value = atoi(lvalue.c_str());
                // std::cout << "Given process wait time = " << delay_value << std::endl;
                location = location +2;
                break;
             case 'c':
                 if(location >= argc) {
                    k3 = 20;
                    // std::cout << "Default coordinates value =  = " << k3 << std::endl;
                    break;
                 }
                 cvalue = argv[location];
                 if(cvalue.at(0) == '-') {
                   k3 = 20;
                   // cout << "Default coordinates value = " << k3 << endl;
                   location++;
                    break;
                }
                k3 = atoi(cvalue.c_str());
                // std::cout << "Given coordinaes value = " << k3 << std::endl;
                location = location +2;
                break;
            default:
                    return 0;

        }
        int c1 = k3;
        int c2 = -k3;
        //cout << "( " << c1 << " , " << c2 << ")" << endl;

        creatingStreets(k1,k2,k3);

         for (int i = 0; i < allStreetCommands.size(); i++){
            cout << allStreetCommands[i] << endl;
        }

        cout << "g" << endl;

        int delay;

        if (delay_value == 5){
                delay = 5;
        }
        else{
            delay = randomNos(delay_value,5);
        }

        delay = delay * 1000;

        //cout << delay << endl;

        usleep(delay);

        for (int x = 0; x < removeStreetNames.size(); x++){
            cout << removeStreetNames[x] << endl;
        }


  return 0;
}
