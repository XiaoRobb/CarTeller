package handler;

import android.content.Context;
import android.os.Looper;
import android.util.Log;
import android.webkit.ConsoleMessage;

import com.shashank.platform.loginui.LoginActivity;
import com.shashank.platform.loginui.RegisterActivity;

import org.json.JSONObject;

import java.io.Console;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public  class HttpHandler {
    final static String URL = "http://apdo.ltd:8000";

}