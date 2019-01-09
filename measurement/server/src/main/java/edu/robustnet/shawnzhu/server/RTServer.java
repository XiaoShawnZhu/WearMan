package edu.robustnet.shawnzhu.server;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.TimeUnit;


public class RTServer {
    private static final long CHUNK_INTERVAL = TimeUnit.MILLISECONDS.toMillis(160);
    private static final long CHUNK_ALL_TIME = TimeUnit.SECONDS.toMillis(600);
    private static final int CHUNK_SIZE = 3000;
    private static final int SOCKET_PORT = 7000;

    public static void main(String args[])throws Exception
    {
        ServerSocket mySocket = new ServerSocket(SOCKET_PORT);
        System.out.println("Listening on port " + SOCKET_PORT + "\n");
        while(true){
            multiChunkDownload(mySocket);
        }

    }

    public static void fillData(byte[] data) {
        for (int i = 0; i < CHUNK_SIZE; i++) {
            data[i] = (byte)(65 + i % 26);
        }
    }

    public static void setSeq(int seq, byte[] data) {
        for (int i = 3; i >= 0; i--) {
            data[i] = (byte)(seq % 256);
            seq /= 256;
        }
    }

    public static int decodeSeq(byte[] bytes) {
        int seq = 0;
        int byteValue = 0;
        for (int i = 0; i < 4; i++) {
            seq *= 256;
            byteValue = ((int)(bytes[i]) + 256) % 256;
            seq += byteValue;
        }
        return seq;
    }

    public static void multiChunkDownload(ServerSocket mySocket)
    {
        int bytes = 0;
        int bytesAll = 0;
        byte[] bytesArray = new byte[4];
        StringBuffer sb = new StringBuffer();

        int seq = 0;
        byte[] data = new byte[CHUNK_SIZE];
        fillData(data);
        long sleepTime;

        // receive request from client
        Socket clientSocket = null;

        try {
            clientSocket = mySocket.accept();
            System.out.println("Connected to " + clientSocket + "\n");
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Socket initiation failed.");
            return;
        }

        try {

            DataOutputStream outToClient = new DataOutputStream(clientSocket.getOutputStream());
            InputStream inputStream = clientSocket.getInputStream();

            System.out.println("Data stream initialized at "+System.currentTimeMillis());

            while (bytesAll < 4) {
                bytes = inputStream.read(bytesArray, bytesAll, 4 - bytesAll);
                bytesAll += bytes;
                System.out.println("bytes changed to " + bytes);
            }

            seq = decodeSeq(bytesArray);

            System.out.println("Starting seq: " + seq);
            long startTime = System.currentTimeMillis();
            long chunkStartTime = startTime;

            while (chunkStartTime - startTime < CHUNK_ALL_TIME) {
                setSeq(seq, data);
                seq++;
                System.out.println("seq updated to " + seq);
                inputStream.available();
                outToClient.write(data);
                outToClient.flush();
                sb.append(System.currentTimeMillis() + "\t" + SOCKET_PORT +"\tTCP\t" + seq + "\t" + CHUNK_SIZE + "\n");

                sleepTime = chunkStartTime + CHUNK_INTERVAL - System.currentTimeMillis();
                if (sleepTime > 0) {
                    Thread.sleep(sleepTime);
                }
                chunkStartTime = System.currentTimeMillis();
                System.out.println("chunkStartTime updated to " + chunkStartTime);

            }
            outToClient.close();
        } catch (IOException e) {
            System.out.println("IOException caught");
            e.printStackTrace();
        } catch (InterruptedException e) {
            System.out.println("InterruptedException caught");
            e.printStackTrace();
        }

        System.out.println("Finished chunk downloads at" + System.currentTimeMillis() + "\n");

    }

}
