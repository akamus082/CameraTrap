///////////////////////////
// The following URLs may not work all the time.
// please open them in a web browser to test the connections.
//
// Alireza Khodamoradi, akhodamo@ucsd.edu
///////////////////////////
#include "main.h"
#include <Awesomium/WebCore.h>
#include <Awesomium/BitmapSurface.h>
#include <Awesomium/STLHelpers.h>

#define WIDTH   1024
#define HEIGHT  768

#define URL_koala           "http://zssd-panda.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=zssd-koala"
#define URL_ape             "http://polarplunge.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=ape"
#define URL_panda           "http://zssd-panda.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=zssd-panda"
#define URL_condor          "http://zssd-condor.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=zssd-condorhd"
#define URL_polar           "http://polarplunge.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=polarplunge"
#define URL_elephant        "http://elephants.player.camzonecdn.com/v1.0/CamzoneStreamPlayer?iframe=yes&channel=elephants"
#define URL_wolf_1          "http://embed.wildearth.tv:8080/cam/mw1den.stream?aspectratio=16:9&zone=36&sourceid=149-114-113-113-11&autostart=true"
#define URL_wolf_2          "http://embed.wildearth.tv:8080/cam/atkaoutside.stream?aspectratio=4:3&zone=36&sourceid=146-114-113-113-11&autostart=true"
#define URL_wolf_Mexican    "http://embed.wildearth.tv:8080/cam/mw1outside.stream?aspectratio=4:3&zone=36&sourceid=150-114-113-113-11&autostart=true"
#define URL_wolf_red        "http://embed.wildearth.tv:8080/cam/rw1den.stream?aspectratio=16:9&amp;zone=36&amp;sourceid=147-114-113-113-11&amp;autostart=true"

using namespace cv;
using namespace std;
using namespace Awesomium;

//g++ -o netcaptest `pkg-config opencv --cflags` main.cpp `pkg-config opencv --libs`  -lawesomium-1-7

int main(int argc, char* argv[])
{
    int i;
    namedWindow("Frame");
    ////////////////////////////////////////////////////
    Mat frame_4, frame;

    //double dWidth = 640; //get the width of frames of the video
    //double dHeight = 480; //get the height of frames of the video
    

    

    vector<Mat> layers;
    WebCore* web_core = WebCore::Initialize(WebConfig());
    WebView* view = web_core->CreateWebView(WIDTH, HEIGHT);
    WebURL url(WSLit(URL_polar));
    view->LoadURL(url);
    BitmapSurface* surface;

    Size frameSize(static_cast<int>(WIDTH), static_cast<int>(HEIGHT));
    VideoWriter writer ("polarbearchillin.avi", CV_FOURCC('D','I','V','3'), 15, frameSize, true); //initialize the VideoWriter object 


    for(int i=0; i<1000000; i++) //delay is added to pass advertisement on some of the URLs
    {
        web_core->Update();
    }
    ///////////////////////////////////////////////////

    if ( !writer.isOpened() ) //if not initialize the VideoWriter successfully, exit the program
    {
        cout << "ERROR: Failed to write the video" << endl;
        return -1;
    }

    while(i != 27)
    {
        ////////////////////////////////////////////////

        web_core->Update();
        surface = (BitmapSurface*)view->surface();
        frame_4 = Mat(Size(WIDTH, HEIGHT), CV_8UC4, (unsigned char*)surface->buffer(), Mat::AUTO_STEP);
        split(frame_4, layers);
        layers.pop_back();
        merge(layers, frame);

        ////////////////////////////////////////////////
        writer.write(frame); //writer the frame into the file
        imshow("Frame", frame);
        i=waitKey(30);
    }
    ///////////////////////
    view->Destroy();
    WebCore::Shutdown();
    ///////////////////////
    destroyAllWindows();
    return 0;
}
