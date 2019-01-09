package edu.robustnet.shawnzhu.wearman;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkInfo;
import android.os.SystemClock;
import android.util.Log;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.concurrent.TimeUnit;

public class ConnectivityLogger extends IntentService {
    private static final String TAG = "ConnectivityLogger";
    private static final long LOG_TIME = TimeUnit.MINUTES.toMillis(5);
    private static final long LOG_INTERVAL_MILLIS = 200;
    ConnectivityManager mConnectivityManager;
    StringBuffer mStringBuffer;

    @Override
    protected void onHandleIntent(Intent arg0) {

        Log.i(TAG, "Intent Service started on ConnectivityLogger");
        mConnectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        long startTime = System.currentTimeMillis();
        mStringBuffer = new StringBuffer();
        try {
            PrintWriter printWriter = new PrintWriter(new FileWriter("/sdcard/connectivity"+System.currentTimeMillis()+".log"));
            while(System.currentTimeMillis() - startTime < LOG_TIME){
                mStringBuffer.append(System.currentTimeMillis());
                mStringBuffer.append("\t");
                Network[] allNetworks = mConnectivityManager.getAllNetworks();
                int i = 0;
                for (Network eachNetwork : allNetworks) {
                    i += 1;
                    NetworkInfo info = mConnectivityManager.getNetworkInfo(eachNetwork);
                    mStringBuffer.append(i);
                    mStringBuffer.append("\t");
                    mStringBuffer.append(info.getTypeName());
                    mStringBuffer.append("\t");
                    mStringBuffer.append(mConnectivityManager.getLinkProperties(eachNetwork).getInterfaceName());
                    mStringBuffer.append("\t");
                    mStringBuffer.append(info.isAvailable());
                    mStringBuffer.append("\t");
                    mStringBuffer.append(info.isConnected());
                    mStringBuffer.append("\t");
                    mStringBuffer.append(info.isFailover());
                    mStringBuffer.append("\t");
                }
                printWriter.println(mStringBuffer);
                mStringBuffer.setLength(0);
                SystemClock.sleep(LOG_INTERVAL_MILLIS);
            }
            printWriter.close();
        } catch (Exception e) {

        }

    }

    public ConnectivityLogger() {
        super("MyIntentService");
    }
}
