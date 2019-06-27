#ifdef VIA_OPENCV

#ifndef USRGAMECONTROLLER_H
#define USRGAMECONTROLLER_H

#include "qtcyberdip.h"

#define WIN_NAME "Frame"

//��Ϸ������
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
	int imgcounter;		//����10֡ͼƬ���ٴ���ȷ���ȶ���
	int getInit;
	int move;
	int swtch;
	initPos init;
	leftDownPos leftDown;
	double pix_dist;
	double len;
	
	cv::Mat coinFrame;
	cv::Mat grayFrame;

//������Ϊ��ʵ�ֿ�����ʾЧ�������ӵ�����
public:
	//���캯�������б����ĳ�ʼ����Ӧ�ڴ����
	usrGameController(void* qtCD);
	//�������������ձ���������Դ
	~usrGameController();
	//����ͼ������ÿ���յ�ͼ��ʱ�������
	int usrProcessImage(cv::Mat& img);

	void detectCir();
	void detectLeftDown(cv::Mat& gray);
	void setInitInfo(cv::Mat& gray);
	void setInit();
	int test(cv::Mat& img);
};


#endif
#endif