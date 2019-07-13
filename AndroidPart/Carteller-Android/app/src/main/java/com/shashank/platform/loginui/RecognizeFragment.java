package com.shashank.platform.loginui;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.text.Selection;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class RecognizeFragment extends Fragment {

    public static final String ARG_TITLE = "titleArg";
    public static final String ARG_INDEX = "indexArg";

    boolean hasSelected = false;

    private Handler handler = new Handler() {
        //处理服务器返回的json
        //根据调用不同的API来以不同方式解析json
        public void handleMessage(Message msg) {
            if(msg.what == -1){
                Toast.makeText( getActivity(),msg.obj.toString() ,Toast.LENGTH_SHORT).show();
            }else {
            try {
                JSONObject jobj = new JSONObject(msg.obj.toString());
                if (msg.what == 1) {
                    TextView resultWord = getActivity().findViewById(R.id.resultWords);
                    resultWord.setText(jobj.getString("msg"));
                } else if (msg.what == 2) {
                    TextView resultWord = getActivity().findViewById(R.id.resultWords);
                    resultWord.setText(jobj.getString("msg"));
                } else if (msg.what == 3) {
                    Gson gson = new Gson();
                    CarInfo carInfo = gson.fromJson(jobj.getString("msg"), CarInfo.class);
//                    String s = "Log_id:"+carInfo.getLog_id() +",num:"+carInfo.getVehicle_num() +",Vechile Info:";
//                    for(CarInfo.VehicleInfoBean c : carInfo.getVehicle_info()){
//                        s+=",Attributes:" +"CopiLot:" + c.getAttributes().getCopilot()
//                                + ",Copilot_visor："+ c.getAttributes().getCopilot_visor()
//                                +",Copilot_belt："+ c.getAttributes().getCopilot_belt()+
//                                ",Copilot_visor："+ c.getAttributes().getDirection().getName() + ":"
//                       + ",Copilot_visor："+ c.getAttributes().getDriver_belt().getScore()
//                        +",Copilot_visor："+ c.getAttributes().getIn_car_item().getScore()
//                                +",Copilot_visor："+ c.getAttributes().getCopilot_visor()
//                        +",Copilot_visor："+ c.getAttributes().getCopilot_visor()
//                        +",Copilot_visor："+ c.getAttributes().getCopilot_visor();
//                        s+=",Location:"+c.getLocation();
//                    }
                    TextView resultWord = getActivity().findViewById(R.id.resultWords);
                    resultWord.setText(jobj.getString(jobj.getString("msg")));
                } else if (msg.what == 4) {
                    TextView resultWord = getActivity().findViewById(R.id.resultWords);
                    resultWord.setText(jobj.getString("msg"));
                } else if (msg.what == 5) {
                    TextView resultWord = getActivity().findViewById(R.id.resultWords);
                    resultWord.setText(jobj.getString("msg"));
                }
            } catch (Exception e) {
                Toast.makeText(getActivity(), "识别失败！请换图重试", Toast.LENGTH_SHORT).show();
            }
            }
        }

    };

    public static RecognizeFragment newInstance(String title, int index) {
        RecognizeFragment ra = new RecognizeFragment();
        Bundle args = new Bundle();
        args.putString(ARG_TITLE, title);
        args.putInt(ARG_INDEX, index);
        ra.setArguments(args);
        return ra;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_recognize, container, false);
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        final ImageButton searchBtn = getActivity().findViewById(R.id.tellBtn);
        final ImageView selectImg = getActivity().findViewById(R.id.selectImage);
        TextView resultWord = getActivity().findViewById(R.id.resultWords);
        final ImageView resultImage = getActivity().findViewById(R.id.resultImage);
        final Spinner spinner = getActivity().findViewById(R.id.spinner);

        searchBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                //将图片上传到服务器并返回结果,应先判断图片是否已经上传
                if (hasSelected) {
                    //上传图片到服务器
                    String b64 = bitmap2String(img);
                    String type = spinner.getSelectedItem().toString();
                    String uname = LoginActivity.username;
                    if (type.equals("车牌识别")) {
                        ImageRequest(RecognizeFragment.this, "/carboard", uname, b64);
                    } else if (type.equals("多车检测")) {
                        ImageRequest(RecognizeFragment.this, "/cartypemore", uname, b64);
                    } else if (type.equals("车型识别")) {
                        ImageRequest(RecognizeFragment.this, "/carinfo", uname, b64);
                    } else if (type.equals("属性识别")) {
                        ImageRequest(RecognizeFragment.this, "/carattribute", uname, b64);
                    } else if (type.equals("违规检测")) {
                        ImageRequest(RecognizeFragment.this, "/carBehavior", uname, b64);
                    } else {

                    }

                } else {
                    Toast.makeText((getActivity()), "请先选择图片！", Toast.LENGTH_SHORT).show();
                }
            }
        });

        selectImg.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                //从相册上传图片，并转为base64,更改上传状态为true
                Intent intent = new Intent(Intent.ACTION_PICK, null);
                intent.setDataAndType(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, "image/*");
                startActivityForResult(intent, 2);
                Toast.makeText(getActivity(), "选择成功！", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public static String bitmap2String(Bitmap bitmap) {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, bos);//参数100表示不压缩
        byte[] bytes = bos.toByteArray(); //Base64算法加密，当字符串过长（一般超过76）时会自动在中间加一个换行符，字符串最后也会加一个换行符。
        // 导致和其他模块对接时结果不一致。所以不能用默认Base64.DEFAULT，而是Base64.NO_WRAP不换行
        return "," + new String(Base64.encode(bytes, Base64.NO_WRAP));
    }

    Bitmap img = null;

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 2) {
            // 从相册返回的数据
            if (data != null) {
                try {
                    // 得到图片的全路径
                    Uri uri = data.getData();
                    ((ImageView) getActivity().findViewById(R.id.selectImage)).setImageURI(uri);
                    img = BitmapFactory.decodeStream(getActivity().getContentResolver().openInputStream(uri));
                    hasSelected = true;
                } catch (FileNotFoundException e) {
                    Toast.makeText(getContext(), "图片不存在！", Toast.LENGTH_SHORT).show();
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        }
    }

    private void ImageRequest(final RecognizeFragment rf, final String suffixURL, String username, String image) {
        String URL = LoginActivity.URL + suffixURL;
        //post方式提交的数据
        FormBody formBody = new FormBody.Builder()
                .add("username", username)
                .add("image", image)
                .build();


        //请求组合创建
        final Request request = new Request.Builder()
                .url(URL)
                .post(formBody)
                .build();
        //发起请求
        OkHttpClient mOkHttpClient = new OkHttpClient();
        mOkHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                handler.obtainMessage(-1, e);
            }

            @Override
            public void onResponse(Call call, Response response) {
                //获得返回，并使用FastJson将Json字符串存储在JavaBean对象中
                try {
                    //用handler对象处理返回消息
                    String json = response.body().string();
                    if (suffixURL.equals("/carboard")) {
                        handler.obtainMessage(1, json).sendToTarget();
                    } else if (suffixURL.equals("/cartypemore")) {
                        handler.obtainMessage(2, json).sendToTarget();
                    } else if (suffixURL.equals("/carattribute")) {
                        handler.obtainMessage(3, json).sendToTarget();
                    } else if (suffixURL.equals("/carinfo")) {
                        handler.obtainMessage(4, json).sendToTarget();
                    } else if (suffixURL.equals("/driverBehavior")) {
                        handler.obtainMessage(5, json).sendToTarget();
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    //登录成功时此方法被调用
    public void onSuccess() {

    }

    public void onFailure() {
        Toast.makeText(getActivity(), "识别失败，请检查网络后重试", Toast.LENGTH_SHORT).show();
    }
}
