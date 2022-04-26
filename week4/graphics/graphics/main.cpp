#include <iostream>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

void dda(){
    // create window
    Mat img(1000, 1000, CV_8UC3, Scalar(0, 0, 0));
    
    int x1, x2, y1, y2, steps;
    cout << "(x1, y1): ";
    cin >> x1 >> y1;
    cout << "(x2, y2): ";
    cin >> x2 >> y2;
    
    int dx = x2 - x1, dy = y2 - y1;
    
    if (dx >= dy)
        steps = dx;
    else
        steps = dy;
    
    int xincrements = dx/steps, yincrements = dy/steps;
    
    vector <int> xcoordinates, ycoordinates;
    
    int i = 0;
    while(i < steps){
        i++;
        
        x1 += xincrements;
        y1 += yincrements;
        
        cout << "x1: " << x1 << ", y1: " << y1 << "\n";
        
        xcoordinates.push_back(x1);
        ycoordinates.push_back(y1);
    }
    
    Point p1 = Point(xcoordinates[0], ycoordinates[0]);
    Point p2 = Point(xcoordinates[xcoordinates.size() - 1], ycoordinates[ycoordinates.size() - 1]);
    
    line(img, p1, p2, Scalar(255, 255, 255), 1);
    
    imshow("DDA Algorithm", img);
    waitKey(0);
    
}

int main(){
    /*
    // empty window
    Mat img(300, 300, CV_8UC3, Scalar(255, 0, 0));
    
    Mat imgResize;
    resize(img, imgResize, Size(600, 500));
    
    // circle(이미지 삽입할 객체, 원의 중심점, 원의 반지름, 원의 색, 원의 꽉참 유무
    circle(imgResize, Point(150, 150), 20, Scalar(0, 255, 0), 5);
    rectangle(imgResize, Point(20, 20), Point(280, 280), Scalar(0, 0, 255), 5);
    line(img, Point(280, 20), Point(20, 280), Scalar(0, 0, 0), 5);
    putText(img, "Hi", Point(50, 40), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 0.5);
    
    Rect roi(50, 50, 200, 200);
    
    Mat ImgCrop = img(roi);
    
    imshow("Basic", img);
    imshow("roi", ImgCrop);
    waitKey(0);
    */
    
    dda();
    
    return 0;
    
}
