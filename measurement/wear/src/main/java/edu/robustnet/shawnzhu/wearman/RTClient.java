package edu.robustnet.shawnzhu.wearman;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class RTClient {

    private static final String TAG = "RTClient";
    private static final int SOCKET_PORT = 7000;
    private static final int RCV_BUF_SIZE = 4096;
    private String socketAddr;
    private Socket socket = null;
    private InputStream inputStream = null;
    private OutputStream outputStream = null;
    private int btDown = 0;
    private ConnectivityManager mConnectivityManager;
    private int thisSeq = 0;

    public void communicate(String socketAddr, Context context) {
        this.socketAddr = socketAddr;
        mConnectivityManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        new communicate().start();
    }

    public class communicate extends Thread {

        @Override
        public void run() {

            while (true) {
                if ((btDown == 1) && !isNetworkAvailable(ConnectivityManager.TYPE_WIFI))
                    continue;
                try {
                    byte[] rcvBuf = new byte[RCV_BUF_SIZE];
                    socket = new Socket();

                    try {
                        Thread.sleep(1000);
                        socket.connect(new InetSocketAddress(socketAddr, SOCKET_PORT));
                        if(btDown==1)
                            Log.d(TAG, "Switched from BT to WiFi");
                        Log.d(TAG, "Connected to " + socketAddr + ":" + SOCKET_PORT + "\n");
                        inputStream = socket.getInputStream();
                        outputStream = socket.getOutputStream();
                    } catch (IOException e) {
                        e.printStackTrace();
                        System.exit(0);
                    }
                    // send starting SEQ
                    byte[] seqByte = new byte[4];
                    encodeSeq(thisSeq, seqByte);
                    outputStream.write(seqByte);
                    outputStream.flush();
                    Log.d(TAG, "SEQ sent: " + thisSeq);
                    download(rcvBuf, socket);

                } catch (Exception e) {
                    genErrorMessage("TCP exception, BT down.");
                    btDown = 1;
                    System.out.println(e);
                }
            }

        }
    }

    public void download(byte rcvBuf[], Socket socket) throws Exception {
        int bytesRead = 0;
        InputStream inputStream = socket.getInputStream();

        try {
            while (bytesRead != -1) {
                bytesRead = inputStream.read(rcvBuf);
                thisSeq++;
                Log.d(TAG, "Expected seq ==> " + thisSeq);
            }
            socket.close();
        } catch (Exception e) {
            Log.d(TAG, "BT down: exception came up");
            btDown = 1;
        }
    }

    public void encodeSeq(int seq, byte[] bytes) {
        for (int i = 3; i >= 0; i--) {
            bytes[i] = (byte) (seq % 256);
            seq /= 256;
        }
    }

    public void genErrorMessage(String netType) {
        Log.d(TAG, netType);

    }

    public boolean isNetworkAvailable(int netType) {

        NetworkInfo netInfo = mConnectivityManager.getNetworkInfo(netType);
        if (netInfo != null) {
            if(netInfo.isConnected()){
                Log.d(TAG, "Network connected.");
                return true;
            }
            else
                return false;
        } else {
            return false;
        }
    }
}
