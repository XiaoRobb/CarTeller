package com.shashank.platform.loginui;

import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.IOException;

import handler.HttpHandler;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class LoginActivity extends AppCompatActivity {

    static String username;
    String session;

    ImageView imageView;
    TextView textView;
    int count = 0;
    Button login;
    Button register;
    EditText uname;
    EditText pwd;
    final static String URL = "http://42.159.89.231:8000";

    private Handler handler= new Handler(){
        //处理服务器返回的json
        public void handleMessage(Message msg){
            if(msg.what == 1) {
                try {

                    JSONObject obj = new JSONObject(msg.obj.toString());
                    String returnName = obj.getString("username");
                    if (returnName.equals("-1")) {
                        onSuccess("", false);
                    } else {
                        username = returnName;
                        onSuccess(obj.getString("session"), true);
                    }
                } catch (Exception e) {
                    Log.d("handler", "handleMessage: "+e.toString());
                }
            }
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        textView = findViewById(R.id.textView);
        //滑动切换背景动画


        imageView.setOnTouchListener(new OnSwipeTouchListener(getApplicationContext()) {
            public void onSwipeTop() {
            }

            public void onSwipeRight() {

                if (count == 0) {
                    imageView.setImageResource(R.drawable.good_night_img);
                    count = 1;
                } else {
                    imageView.setImageResource(R.drawable.good_morning_img);
                    count = 0;
                }
            }

            public void onSwipeLeft() {
                if (count == 0) {
                    imageView.setImageResource(R.drawable.good_night_img);
                    count = 1;
                } else {
                    imageView.setImageResource(R.drawable.good_morning_img);
                    count = 0;
                }
            }

            public void onSwipeBottom() {
            }

        });

        //绑定
        login = findViewById(R.id.Login);
        register = findViewById(R.id.Register);
        uname = findViewById(R.id.lusername);
        pwd = findViewById(R.id.lpassword);

        this.login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //进行登录操作
                loginRequest(LoginActivity.this,  uname.getText().toString(),pwd.getText().toString());
            }
        });

        this.register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //转入注册页面
                Intent it = new Intent(LoginActivity.this,RegisterActivity.class);
                startActivity(it);

            }
        });
    }

        //登录成功时此方法被调用
        public void onSuccess(String session, Boolean is_succ){
            this.session = session;
            if(is_succ){
                Toast.makeText(LoginActivity.this, "登录成功！",Toast.LENGTH_SHORT ).show();
                //转入主界面，将session同时传递过去
                Intent intent = new Intent(this,SelectionActivity.class);
                intent.putExtra("session",session).putExtra("username",username);
                startActivity(intent);

            }else{
                //成功返回，但是账号或者密码有问题
                Toast.makeText(LoginActivity.this, "账号或密码错误！请重试",Toast.LENGTH_SHORT).show();
            }
        }

        public void onFailure(){
        Toast.makeText(LoginActivity.this,"登录失败，请检查网络后重试",Toast.LENGTH_SHORT).show();
        }

    void loginRequest(final LoginActivity login, String name, String pwd) {

        FormBody formBody = new FormBody.Builder()
                .add("username", name)
                .add("password", pwd)
                .build();
        //请求组合创建
        final Request request = new Request.Builder()
                .url(URL + "/login")
                .post(formBody)
                .build();
        //发起请求
        OkHttpClient mOkHttpClient = new OkHttpClient();
        mOkHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                //请求失败时
                login.onFailure();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                //请求返回时,返回json，进行判断
                try {
                    String json = response.body().string();
                    handler.obtainMessage(1,json).sendToTarget();

                } catch (Exception e) {
                    Log.d("onsucc", e.toString());
                }
            }
        });
    }
}


