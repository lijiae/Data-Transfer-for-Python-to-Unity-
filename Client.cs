using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class Client : MonoBehaviour
{
    // Start is called before the first frame update
    private string message;
    private Socket client;
    private string host = "127.0.0.1";
    private int port = 10086;
    private byte[] messTmp;
    int mysym=0;//连接成功
    Thread ConnectThread;
    PosiSet mes;
    int SumLen = 0;


    [Tooltip("判断是否重播")]
    [SerializeField]//显示私有变量
    private bool isDateBack;

    public Slider timeLine;


    public void InitSocket(){
        ConnectThread=new Thread(new ThreadStart(GetMessage));
        ConnectThread.Start();
       // Cursor.visible = false;
        Debug.Log("执行了");
    }

    void SocketConnect(){
        if(client!=null)
            client.Close();
        try{
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        client.Connect(new IPEndPoint(IPAddress.Parse(host), port));
        Debug.Log("Connecting Success");

        }
        catch(Exception){
            Debug.Log("Connecting Fail");
            return;
        }
    }
    PosiSet ReadToObject(string json)
    {
        PosiSet deserializedUser = new PosiSet();               
        deserializedUser = (PosiSet)JsonUtility.FromJson<PosiSet>(json);
        return deserializedUser;
    }

    public void TransData(PosiSet set){
        //GameObject.Find("需要传递到游戏对象的Name").SendMessage("脚本中的方法名称",Object//传递的参数类型,SendMessageOptions.DontRequireReceiver）;
        GameObject.Find("BridgeHouse").GetComponent<Control>().ReceiveData(set);
    }

    void GetMessage()
    {
        SocketConnect();
       
        while(true){ 
        messTmp = new byte[2048];
        int count = client.Receive(messTmp);//长度
        if (count == 0)
        {
            continue;
        }
            SumLen = SumLen + count;
            mes = ReadToObject(Encoding.UTF8.GetString(messTmp, 1, count-2));
            //Debug.Log(mes.ToString());

            StoredInfo.Instance.allInfo.Add(mes);


            Array.Clear(messTmp, 0, count);
            mysym=1;
        
        }
    }

    //加个slider在值的变化里判断
    //isDateBack = true;

    public void OnTimeLineChanged()//当时间轴被拖动的时候
    {
        if (timeLine.value > 0.98f)
        {
            timeLine.value = 1;
            isDateBack = false;

        }
        else
        {
            isDateBack = true;
            DateBack(timeLine.value);

        }



    }


    public void DateBack(float value)//用于回放的方法
    {
        if (StoredInfo.Instance.allInfo.Count != 0)
        {
            PosiSet oldData = StoredInfo.Instance.GetOldData(value);
            TransData(oldData);

        }

    }



    public void SocketQuit(){
        if(ConnectThread!=null)
        {
            ConnectThread.Interrupt();
            ConnectThread.Abort();
        }

        if(client!=null){
            client.Close();
        }
        Application.Quit();
    }

    void Start()
    {
        //InitSocket();
        //Cursor.visible = false;
    }
    // Update is called once per frame
    void Update()
    {
        if (mysym == 1 && !isDateBack)
            TransData(mes);
    }

}
