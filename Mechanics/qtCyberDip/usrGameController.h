#ifdef VIA_OPENCV

#ifndef USRGAMECONTROLLER_H
#define USRGAMECONTROLLER_H

#include "qtcyberdip.h"

#define WIN_NAME "Frame"

//游戏控制类
class usrGameController{
private:
	deviceCyberDip* device;

	struct initPos {
		int x;
		int y;
		int up_x;
		int up_y;
		int down_x;
		int down_y;
		initPos() : x(0), y(0), up_x(0), up_y(0), down_x(0), down_y(0) { ; }
	};

	struct leftDownPos {
		int x;
		int y;
		leftDownPos() : x(0), y(0) { ; }
	};
	
	int flag_0;
	int counter_0;
	int counter_1;
	int taskEnd;
	int initDone;
	int imgcounter;		//接收10帧图片后再处理，确保稳定性
	int getInit;
	int move;
	int swtch;
	initPos init;
	leftDownPos leftDown;
	double pix_dist;
	double len;
	
	cv::Mat coinFrame;
	cv::Mat grayFrame;

//以上是为了实现课堂演示效果，增加的内容
public:
	//构造函数，所有变量的初始化都应在此完成
	usrGameController(void* qtCD);
	//析构函数，回收本类所有资源
	~usrGameController();
	//处理图像函数，每次收到图像时都会调用
	int usrProcessImage(cv::Mat& img);

	void detectCir();
	void detectLeftDown(cv::Mat& gray);
	void setInitInfo(cv::Mat& gray);
	void setInit();
	int test(cv::Mat& img);
};


#endif
#endif