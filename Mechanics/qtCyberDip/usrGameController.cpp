#include "usrGameController.h"

#ifdef VIA_OPENCV
//构造与初始化
usrGameController::usrGameController(void* qtCD)
{
	qDebug() << "usrGameController online.";
	device = new deviceCyberDip(qtCD);//设备代理类
	//device->comMoveToScale(0.5, 0.5);
	//device->comMoveTo(-5, -5);
	device->comHitUp();
	cv::namedWindow(WIN_NAME);
	//cv::setMouseCallback(WIN_NAME, mouseCallback, (void*)&(argM));
	
	flag_0 = 1;
	counter_0 = 0;
	counter_1 = 0;
	taskEnd = 1;
	initDone = 0;
	imgcounter = 0;
	move = 0;
	getInit = 0;
	pix_dist = 0.0;
	len = 232;		// ipad 实际边长，单位mm
	swtch = 1;
}

//析构
usrGameController::~usrGameController()
{
	cv::destroyAllWindows();
	if (device != nullptr)
	{
		delete device;
	}
	qDebug() << "usrGameController offline.";
}

//处理图像 
int usrGameController::usrProcessImage(cv::Mat& img)
{
	cv::Size imgSize(img.cols, img.rows - UP_CUT);
	if (imgSize.height <= 0 || imgSize.width <= 0)
	{
		qDebug() << "Invalid image. Size:" << imgSize.width <<"x"<<imgSize.height;
		return -1;
	}

	//if (!initDone)
	//{
	//	device->comMoveTo(-35, 25);
	//	initDone = 1;
	//}


	////截取图像边缘
	//cv::Mat pt = img(cv::Rect(0, UP_CUT, imgSize.width,imgSize.height));
	////cv::imshow(WIN_NAME, pt);


	if (imgcounter < 10) 
	{
		imgcounter++;
		return 1;
	}
	
	if (!getInit) 
	{
		device->comHitUp();
		std::this_thread::sleep_for(std::chrono::seconds(1));
		cv::imwrite("C:/Users/15308/Desktop/data_0.png", img);
		cv::Mat gray;
		cv::cvtColor(img, gray, CV_BGR2GRAY);
		std::thread t2(&usrGameController::setInit, this);
		t2.detach();
		getInit = 1;
		return 2;
	}
	if (getInit == 1)
	{
		return 3;
	}
	//else
	//{
	//	int targetx = 0, targety = 0;
	//	targetx = leftdown.x + (double)25 / 25 * (2 * init.radius - 1);
	//	targety = leftdown.y - (double)86 / 25 * (2 * init.radius - 1);
	//	device->commoveto((double)(targety - init.y) * 25 / (2 * init.radius - 1), (double)(targetx - init.x) * 25 / (2 * init.radius - 1));
	//}

	if (taskEnd)
	{
		//std::cout << img.rows << '\t' << img.cols << std::endl;
		//std::thread t1(&usrGameController::detectLeftDown, this, gray);
		std::thread t1(&usrGameController::test, this, img);
		t1.detach();
		taskEnd = 0;
	}
	cv::imshow(WIN_NAME, img);

	return 0;
}


void usrGameController::detectCir()
{
	////std::time_t now = std::time(0);
	////char* dt = ctime(&now);
	////std::cout << "Begin detection " << dt << std::endl;

	//cv::Mat coin = cv::imread("C:/Users/15308/Desktop/coin.png");
	//cv::Mat gray_coin;
	//std::vector<cv::Vec3f> circles;
	//cv::cvtColor(coin, gray_coin, CV_BGR2GRAY);
	//cv::GaussianBlur(gray_coin, gray_coin, cv::Size(3, 3), 1);
	//cv::HoughCircles(gray_coin, circles, CV_HOUGH_GRADIENT, 1, gray_coin.rows / 8, 200, 50);
	////std::cout << "circle size: " << circles.size() << std::endl;
	//for (int i = 0; i < circles.size(); ++i)
	//{
	//	cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
	//	int radius = cvRound(circles[i][2]);
	//	cv::circle(coin, center, 3, cv::Scalar(0, 255, 0), 1, 8, 0);
	//	cv::circle(coin, center, radius, cv::Scalar(155, 50, 255), 1, 8, 0);
	//}
	////cv::imshow("coin", coin);
	////std::this_thread::sleep_for(std::chrono::seconds(3));
	////now = std::time(0);
	////dt = ctime(&now);
	////std::cout << "End detection " << dt << std::endl;
	//coinFrame = coin.clone();
	//taskEnd = 1;
}


void usrGameController::detectLeftDown(cv::Mat& gray)
{
	//int i = 0, j = 0, flag = 2;
	//for (i = 0; i < gray.rows; ++i)
	//{
	//	for (j = 0; j < gray.cols; ++j)
	//	{
	//		gray.at<uchar>(i, j) = (gray.at<uchar>(i, j) < 60) ? 255 : 0;
	//	}
	//}

	//int maxPxInRow = 0, maxPxInCol = 0;
	//for (int i = 0; i < gray.rows; ++i)
	//{
	//	int tmp = 0;
	//	for (int j = 0; j < gray.cols; ++j)
	//	{
	//		if (gray.at<uchar>(i, j))
	//			tmp++;
	//	}
	//	if (tmp > maxPxInRow)
	//		maxPxInRow = tmp;
	//}
	//for (int j = 0; j < gray.cols; ++j)
	//{
	//	int tmp = 0;
	//	for (int i = 0; i < gray.rows; ++i)
	//	{
	//		if (gray.at<uchar>(i, j))
	//			tmp++;
	//	}
	//	if (tmp > maxPxInCol)
	//		maxPxInCol = tmp;
	//}
	////std::cout << "height: " << gray.rows << '\t' << "width: " << gray.cols << std::endl;
	////std::cout << "maxPxInCol: " << maxPxInCol << '\t' << "maxPxInRow: " << maxPxInRow << std::endl;

	//int tmpX, tmpY;
	//for (i = gray.rows - 1; i >-1; --i)
	//{
	//	int pxInRow = 0;
	//	for (j = 0; j < gray.cols; ++j)
	//	{
	//		if (gray.at<uchar>(i, j))
	//			pxInRow++;
	//	}
	//	if (flag == 2 && pxInRow > 150)
	//		flag--;
	//	if (flag == 1 && pxInRow < 100)
	//		flag--;
	//	if (!flag)
	//	{
	//		//tmpY = i;
	//		leftDown.y = i;
	//		flag = 2;
	//		//std::cout << "break, y: " << i << std::endl;
	//		break;
	//	}
	//}
	//for (j = 0; j < gray.cols; ++j)
	//{
	//	int pxInCol = 0;
	//	for (i = 0; i < gray.rows; ++i)
	//	{
	//		if (gray.at<uchar>(i, j))
	//			pxInCol++;
	//	}
	//	if (flag == 2 && pxInCol > 250)
	//		flag--;
	//	if (flag == 1 && pxInCol < 150)
	//		flag--;
	//	if (!flag)
	//	{
	//		//tmpX = j;
	//		leftDown.x = j;
	//		//std::cout << "break, x: " << j << std::endl;
	//		break;
	//	}
	//}

	//std::cout << "leftDown.x: " << leftDown.x << '\t' << "leftDown.y: " << leftDown.y << std::endl;
	//cv::circle(gray, cv::Point(leftDown.x, leftDown.y), 5, cv::Scalar(150), 2, 8, 0);
	//cv::circle(gray, cv::Point(leftDown.x, leftDown.y), 50, cv::Scalar(150), 3, 8, 0);

	//cv::circle(gray, cv::Point(init.x, init.y), 3, cv::Scalar(200), 1, 8, 0);
	//cv::circle(gray, cv::Point(init.x, init.y), init.radius, cv::Scalar(200), 3, 8, 0);
	////cv::namedWindow("gray");
	////cv::imshow("gray", gray);
	////std::this_thread::sleep_for(std::chrono::seconds(3));
	//grayFrame = gray.clone();

	//std::cout << "radius: " << init.radius << std::endl;
	//if (move)
	//{
	//	int targetx = 0, targety = 0, ctrlx = 0, ctrly = 0;
	//	targetx = leftDown.x + (double)25 / 25 * (2 * init.radius - 1);
	//	targety = leftDown.y - (double)86 / 25 * (2 * init.radius - 1);
	//	std::cout << "targetx: " << targetx << '\t' << "targety: " << targety << std::endl;
	//	ctrlx = ((double)(targety) - init.y) * 25 / (2 * init.radius - 1);
	//	ctrly = ((double)(targetx) - init.x) * 25 / (2 * init.radius - 1);
	//	std::cout << "ctrlx: " << ctrlx << '\t' << "ctrly: " << ctrly << std::endl;
	//	//device->comMoveTo((double)(targety - init.y) * 25 / (2 * init.radius - 1), (double)(targetx - init.x) * 25 / (2 * init.radius - 1));
	//}
	//else
	//{
	//	//device->comMoveTo(0, 0);
	//}

	//move = 1 - move;
	//std::this_thread::sleep_for(std::chrono::seconds(2));
	//taskEnd = 1;
}


void usrGameController::setInitInfo(cv::Mat& gray)
{
	//cv::Mat coin = cv::imread("C:/Users/15308/Desktop/coin.png");
	//cv::Mat gray_coin;
	//std::vector<cv::Vec3f> circles;
	//cv::cvtColor(coin, gray_coin, CV_BGR2GRAY);
	//cv::GaussianBlur(gray_coin, gray_coin, cv::Size(3, 3), 1);
	//cv::HoughCircles(gray_coin, circles, CV_HOUGH_GRADIENT, 1, gray_coin.rows / 8, 200, 50);

	std::vector<cv::Vec3f> circles;
	cv::Mat tmp;
	cv::GaussianBlur(gray, tmp, cv::Size(3, 3), 1);
	cv::HoughCircles(tmp, circles, CV_HOUGH_GRADIENT, 1, 20, 50, 30, 30, 40);
	if (circles.size() == 1)
	{
		init.x = circles[0][0];
		init.y = circles[0][1];
		//init.radius = circles[0][2];
	}
	std::cout << "circle size: " << circles.size() << std::endl;
	for (int i = 0; i < circles.size(); ++i)
	{
		cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
		int radius = cvRound(circles[i][2]);
		cv::circle(tmp, center, 3, cv::Scalar(0, 255, 0), 1, 8, 0);
		cv::circle(tmp, center, radius, cv::Scalar(155, 50, 255), 1, 8, 0);
	}
	cv::imwrite("C:/Users/15308/Desktop/detect_cir_0.png", tmp);

	int i = 0, j = 0, flag = 2;
	for (i = 0; i < gray.rows; ++i)
	{
		for (j = 0; j < gray.cols; ++j)
		{
			gray.at<uchar>(i, j) = (gray.at<uchar>(i, j) < 60) ? 255 : 0;
		}
	}

	for (i = gray.rows - 1; i > -1; --i)
	{
		int pxInRow = 0;
		for (j = 0; j < gray.cols; ++j)
		{
			if (gray.at<uchar>(i, j))
				pxInRow++;
		}
		if (flag == 2 && pxInRow > 150)
			flag--;
		if (flag == 1 && pxInRow < 100)
			flag--;
		if (!flag)
		{
			leftDown.y = i;
			flag = 2;
			std::cout << "break, y: " << i << std::endl;
			break;
		}
	}
	for (j = 0; j < gray.cols; ++j)
	{
		int pxInCol = 0;
		for (i = 0; i < gray.rows; ++i)
		{
			if (gray.at<uchar>(i, j))
				pxInCol++;
		}
		if (flag == 2 && pxInCol > 250)
			flag--;
		if (flag == 1 && pxInCol < 150)
			flag--;
		if (!flag)
		{
			leftDown.x = j;
			std::cout << "break, x: " << j << std::endl;
			break;
		}
	}
	getInit = true;


	// 尝试图片传输
}


void usrGameController::setInit()
{
	std::cout << "init begins" << std::endl;
	WSADATA WinSockData;
	int iWsaStartUp;
	int iWsaCleanUp;

	SOCKET UDPSocketClient;
	struct sockaddr_in UDPServer;
	struct sockaddr_in UDPClient;

	char Buffer[100];

	char RecvBuff[100];
	int iBufferLen = strlen(Buffer) + 1;
	int iUDPServerLen = sizeof(UDPServer);
	int iUDPClientLen = sizeof(UDPClient);
	int iSendto;
	int iReceiveFrom;
	int iBind;

	int iCloseSocket;

	// Step-1 initialization of Winsock
	iWsaStartUp = WSAStartup(MAKEWORD(2, 2), &WinSockData);

	if (iWsaStartUp != 0)
	{
		std::cout << "WSAStartUp Fun Failed" << std::endl;
	}
	std::cout << "WSAStartUp Success" << std::endl;


	// Step-2 Fill the UDPServer(SOCKET ADDRESS) Structure
	UDPServer.sin_family = AF_INET;
	//UDPServer.sin_addr.s_addr = inet_addr("192.168.2.104");
	//UDPServer.sin_addr.s_addr = inet_addr("10.162.45.126");
	UDPServer.sin_addr.s_addr = inet_addr("10.162.220.210");
	UDPServer.sin_port = htons(8899);

	// to receive data from server
	UDPClient.sin_family = AF_INET;
	//UDPClient.sin_addr.s_addr = inet_addr("192.168.2.104");
	UDPClient.sin_addr.s_addr = inet_addr("10.162.45.126");
	UDPClient.sin_port = htons(9000);


	// Step-3 Socket Creation
	UDPSocketClient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

	if (UDPSocketClient == INVALID_SOCKET)
	{
		std::cout << "Socket Creation Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Socket Creation Success" << std::endl;


	// Bind
	iBind = bind(UDPSocketClient, (SOCKADDR *)&UDPClient, sizeof(UDPClient));

	if (iBind == SOCKET_ERROR)
	{
		std::cout << "Binding Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Binding Success" << std::endl;

	// Step-4 Sendto Fun

	// 初始化信号
	Buffer[0] = '&';
	//Buffer[1] = '\0';
	iBufferLen = strlen(Buffer) + 1;
	iSendto = sendto(UDPSocketClient, Buffer, iBufferLen, MSG_DONTROUTE, (SOCKADDR *)&UDPServer, sizeof(UDPServer));

	if (iSendto == SOCKET_ERROR)
	{
		std::cout << "Sending Data Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Sending Data Success" << std::endl;


	// Receive
	int data[6];  // init_x, init_y, up_x, up_y, down_x, down_y
	int pp, tp;
	char tmp[5];

	iReceiveFrom = recvfrom(UDPSocketClient, RecvBuff, 100, MSG_PEEK, (SOCKADDR*)&UDPClient, &iUDPClientLen);

	if (iReceiveFrom == SOCKET_ERROR)
	{
		std::cout << "Receiving failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Receiving Success" << std::endl;
	std::cout << "************************" << std::endl;
	std::cout << "Receive Data-> " << RecvBuff << std::endl;
	std::cout << "************************" << std::endl;

	pp = 0;
	tp = 0;
	//std::cout << atoi("100") << std::endl;
	for (int i = 0; i < 100; ++i)
	{
		if (RecvBuff[i] == '+')
		{
			tmp[tp] = '\0';
			tp = 0;
			data[pp++] = atoi(tmp);
			std::cout << data[pp - 1] << std::endl;
			//pp++;
			if (pp == 6)
				break;
		}
		else
		{
			tmp[tp++] = RecvBuff[i];
		}
	}

	init.x = data[0];
	init.y = data[1];
	init.up_x = data[2];
	init.up_y = data[3];
	init.down_x = data[4];
	init.down_y = data[5];
	pix_dist = len / sqrt((init.up_x - init.down_x) * (init.up_x - init.down_x) + (init.up_y - init.down_y) * (init.up_y - init.down_y));
	std::cout << "初始像素 x: " << init.x << "\ty: " << init.y << std::endl;
	std::cout << "相邻像素间对应的实际距离(mm)：" << pix_dist << std::endl;

	// Step-5 CloseSocket Function
	iCloseSocket = closesocket(UDPSocketClient);

	if (iCloseSocket == SOCKET_ERROR)
	{
		std::cout << "Socket closing failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Socket Closing Success" << std::endl;


	// Step-7 WSACleanUp Fun for terminating from DLL
	iWsaCleanUp = WSACleanup();

	if (iWsaCleanUp == SOCKET_ERROR)
	{
		std::cout << "WSA CleanUp failed & Erroe No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "WSA CleanUp Success" << std::endl;

	device->comMoveTo(0, -5);
	//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
	std::this_thread::sleep_for(std::chrono::seconds(1));
	device->comHitOnce();
	std::this_thread::sleep_for(std::chrono::seconds(3));
	//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
	std::cout << "init ends" << std::endl;
	getInit = 2;
}


int usrGameController::test(cv::Mat& img)
{
	std::cout << "height: " << img.rows << "\t" << "width: " << img.cols << std::endl;
	if (!swtch)
	{
		taskEnd = 1;
		return -1;
	}

	WSADATA WinSockData;
	int iWsaStartUp;
	int iWsaCleanUp;

	SOCKET UDPSocketClient;
	struct sockaddr_in UDPServer;
	struct sockaddr_in UDPClient;

	char Buffer[100];

	char RecvBuff[100];
	int iBufferLen = strlen(Buffer) + 1;
	int iUDPServerLen = sizeof(UDPServer);
	int iUDPClientLen = sizeof(UDPClient);
	int iSendto;
	int iReceiveFrom;
	int iBind;

	int iCloseSocket;

	// Step-1 initialization of Winsock
	iWsaStartUp = WSAStartup(MAKEWORD(2, 2), &WinSockData);

	if (iWsaStartUp != 0)
	{
		std::cout << "WSAStartUp Fun Failed" << std::endl;
	}
	std::cout << "WSAStartUp Success" << std::endl;


	// Step-2 Fill the UDPServer(SOCKET ADDRESS) Structure
	UDPServer.sin_family = AF_INET;
	//UDPServer.sin_addr.s_addr = inet_addr("192.168.2.104");
	//UDPServer.sin_addr.s_addr = inet_addr("10.162.45.126");
	UDPServer.sin_addr.s_addr = inet_addr("10.162.220.210");
	UDPServer.sin_port = htons(8899);

	// to receive data from server
	UDPClient.sin_family = AF_INET;
	//UDPClient.sin_addr.s_addr = inet_addr("192.168.2.104");
	UDPClient.sin_addr.s_addr = inet_addr("10.162.45.126");
	UDPClient.sin_port = htons(9000);


	// Step-3 Socket Creation
	UDPSocketClient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

	if (UDPSocketClient == INVALID_SOCKET)
	{
		std::cout << "Socket Creation Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Socket Creation Success" << std::endl;


	// Bind
	iBind = bind(UDPSocketClient, (SOCKADDR *)&UDPClient, sizeof(UDPClient));

	if (iBind == SOCKET_ERROR)
	{
		std::cout << "Binding Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Binding Success" << std::endl;

	// Step-4 Sendto Fun
	
	// 信号
	Buffer[0] = '^';
	//Buffer[1] = '\0';
	iBufferLen = strlen(Buffer) + 1;
	iSendto = sendto(UDPSocketClient, Buffer, iBufferLen, MSG_DONTROUTE, (SOCKADDR *)&UDPServer, sizeof(UDPServer));

	if (iSendto == SOCKET_ERROR)
	{
		std::cout << "Sending Data Failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Sending Data Success" << std::endl;


	// Receive
	int pixel[7];  // mode, x0, y0, x1, y1, x2, y2
	int pp, tp;
	char tmp[5];

	iReceiveFrom = recvfrom(UDPSocketClient, RecvBuff, 100, MSG_PEEK, (SOCKADDR*)&UDPClient, &iUDPClientLen);

	if (iReceiveFrom == SOCKET_ERROR)
	{
		std::cout << "Receiving failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Receiving Success" << std::endl;
	std::cout << "************************" << std::endl;
	std::cout << "Receive Data-> " << RecvBuff << std::endl;
	std::cout << "************************" << std::endl;

	pp = 0;
	tp = 0;
	//std::cout << atoi("100") << std::endl;
	for (int i = 0; i < 100; ++i)
	{
		if (RecvBuff[i] == '+')
		{
			tmp[tp] = '\0';
			tp = 0;
			pixel[pp++] = atoi(tmp);
			std::cout << pixel[pp - 1] << std::endl;
			//pp++;
			if (pp == 7)
				break;
		}
		else
		{
			tmp[tp++] = RecvBuff[i];
		}
	}

	// 操控机械手
	int mode = pixel[0], x0 = pixel[1], y0 = pixel[2], x1 = pixel[3], y1 = pixel[4], x2 = pixel[5], y2 = pixel[6];
	if (mode == 0)	// 点动物
	{
		std::cout << "开始点动物" << std::endl << std::endl;
		device->comMoveTo((double)(y0 - init.y) * pix_dist, (double)(x0 - init.x) * pix_dist);
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comHitOnce();
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comMoveTo((double)(y1 - init.y) * pix_dist, (double)(x1 - init.x) * pix_dist);
		std::this_thread::sleep_for(std::chrono::seconds(2));
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		device->comHitOnce();
		//std::this_thread::sleep_for(std::chrono::seconds(1));
		std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		device->comMoveTo(0, 0);
		std::this_thread::sleep_for(std::chrono::seconds(3));
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::cout << "第一个点: x: " << x0 << "\ty: " << y0 << std::endl;
		std::cout << "第二个点: x: " << x1 << "\ty: " << y0 << std::endl;
		std::cout << "0 move to: " << "x: " << (double)(y0 - init.y) * pix_dist << "\ty: " << (double)(x0 - init.x) * pix_dist << std::endl;
		std::cout << "1 move to: " << "x: " << (double)(y1 - init.y) * pix_dist << "\ty: " << (double)(x1 - init.x) * pix_dist << std::endl;
		std::cout << "别点动物了" << std::endl << std::endl;
	}
	else
	{
		std::cout << "开始点继续" << std::endl << std::endl;
		device->comMoveTo((double)(y0 - init.y) * pix_dist, (double)(x0 - init.x) * pix_dist);
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comHitOnce();
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comMoveTo((double)(y1 - init.y) * pix_dist, (double)(x1 - init.x) * pix_dist);
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comHitOnce();
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comMoveTo((double)(y2 - init.y) * pix_dist, (double)(x2 - init.x) * pix_dist);
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comHitOnce();
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::this_thread::sleep_for(std::chrono::seconds(2));
		device->comMoveTo(0, 0);
		std::this_thread::sleep_for(std::chrono::seconds(4));
		//std::this_thread::sleep_for(std::chrono::milliseconds(1500));
		std::cout << "第一个点: x: " << x0 << "\ty: " << y0 << std::endl;
		std::cout << "0 move to: " << "x: " << (double)(y0 - init.y) * pix_dist << "\ty: " << (double)(x0 - init.x) * pix_dist << std::endl;
		std::cout << "第二个点: x: " << x1 << "\ty: " << y1 << std::endl;
		std::cout << "0 move to: " << "x: " << (double)(y1 - init.y) * pix_dist << "\ty: " << (double)(x1 - init.x) * pix_dist << std::endl;
		std::cout << "第三个点: x: " << x2 << "\ty: " << y2 << std::endl;
		std::cout << "0 move to: " << "x: " << (double)(y2 - init.y) * pix_dist << "\ty: " << (double)(x2 - init.x) * pix_dist << std::endl;
		std::cout << "别点继续了" << std::endl << std::endl;
	}

	// Step-5 CloseSocket Function
	iCloseSocket = closesocket(UDPSocketClient);

	if (iCloseSocket == SOCKET_ERROR)
	{
		std::cout << "Socket closing failed & Error No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "Socket Closing Success" << std::endl;


	// Step-7 WSACleanUp Fun for terminating from DLL
	iWsaCleanUp = WSACleanup();

	if (iWsaCleanUp == SOCKET_ERROR)
	{
		std::cout << "WSA CleanUp failed & Erroe No-> " << WSAGetLastError() << std::endl;
	}
	std::cout << "WSA CleanUp Success" << std::endl;

	//system("pause");
	//swtch = 0;
	taskEnd = 1;
	return 0;
}


#endif
