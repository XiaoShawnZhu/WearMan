package edu.robustnet.shawnzhu.wearman;

import android.util.Log;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class TCPClient {

    private static final String TAG = "TCPClient";
    private static final int UP = 0;
    private static final int DOWN = 1;
    private static final int MAX_UL_SIZE = 10000000;
    private static final int SOCKET_PORT = 4000;
    private String socketAddr;
    private int totalSize = 0;
    private int fileSize = 0;
    private int direction = UP;
    private int speed = 0;

    public void communicate(int direction, int fileSize, int speed, String socketAddr){
        this.direction = direction;
        this.fileSize = fileSize;
        this.socketAddr = socketAddr;
        this.speed = speed;
        new communicate().start();

    }

    public class communicate extends Thread{
        @Override
        public void run(){
            try{
                if(direction==DOWN)
                    download(fileSize, speed, socketAddr);
                else
                    upload(fileSize, speed, socketAddr);
            }catch (Exception e){
                e.printStackTrace();
            }

        }
    }

    public void download(int fileSize, int speed_bps, String socketAddr) throws Exception {
        int bytesRead = 0;
        Log.d(TAG, "to download");
        byte[] recvBuf = new byte[1024*32];
        Socket socket = new Socket();
        socket.connect(new InetSocketAddress(socketAddr, SOCKET_PORT));
        InputStream inputStream = socket.getInputStream();
        OutputStream outputStream = socket.getOutputStream();
        byte[] buf = new byte[10];

        byte[] size = intToByteArray(fileSize);
        byte[] direction_b = ShortToByteArray(DOWN);
        byte[] speed = intToByteArray(speed_bps);

        System.arraycopy(size, 0, buf, 0, 4);
        System.arraycopy(direction_b, 0, buf, 4, 2);
        System.arraycopy(speed, 0, buf, 6, 4);
        outputStream.write(buf);

        while (totalSize < fileSize) {
            bytesRead = inputStream.read(recvBuf);
            totalSize += bytesRead;
        }

        Log.d(TAG, "Finish");
        socket.close();
        totalSize = 0;
    }

    public void upload(int fileSize, int speed_bps, String socketAddr) throws Exception {

        Log.d(TAG, "to upload");
        int segmentSize = 0;
        byte[] fileBuf = new byte[MAX_UL_SIZE];
        Socket socket = new Socket();
        socket.connect(new InetSocketAddress(socketAddr, SOCKET_PORT));
        OutputStream outputStream = socket.getOutputStream();
        byte[] buf = new byte[10];
        byte[] size = intToByteArray(fileSize);
        byte[] direction_b = ShortToByteArray(UP);
        byte[] speed = intToByteArray(speed_bps);

        System.arraycopy(size, 0, buf, 0, 4);
        System.arraycopy(direction_b, 0, buf, 4, 2);
        System.arraycopy(speed, 0, buf, 6, 4);
        outputStream.write(buf);

        for (int j=0; j<fileSize; j++) {
            fileBuf[j] = (byte)('A' + j % 26);
        }

        while (totalSize < fileSize) {

            if(speed_bps!=0){
                segmentSize = Math.min(500, fileSize-totalSize);
                outputStream.write(fileBuf, totalSize, segmentSize);
                if(speed_bps > 0){
                    Thread.sleep(8*1000*segmentSize/speed_bps);
                }
            }
            else{
                segmentSize = Math.min(1024*32, fileSize-totalSize);
                outputStream.write(fileBuf, totalSize, segmentSize);
            }
            totalSize += segmentSize;
            Log.d(TAG, "Bytes sent: " + totalSize);
        }

        Log.d(TAG, "Finish sending");
        Thread.sleep(5000);
        socket.close();
        totalSize = 0;
    }

    public static final byte[] intToByteArray(int value) {
        // little-endian
        byte[] src = new byte[4];
        src[3] =  (byte) ((value>>24) & 0xFF);
        src[2] =  (byte) ((value>>16) & 0xFF);
        src[1] =  (byte) ((value>>8) & 0xFF);
        src[0] =  (byte) (value & 0xFF);
        return src;
    }

    public static final byte[] ShortToByteArray(int value) {
        // little-endian
        byte[] src = new byte[2];
        src[1] =  (byte) ((value>>8) & 0xFF);
        src[0] =  (byte) (value & 0xFF);
        return src;
    }

}
