package com.shashank.platform.loginui;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;



public class UserinfoFragment extends Fragment {
    public static final String ARG_TITLE = "titleArg";
    public static final String ARG_INDEX = "indexArg";

    public static UserinfoFragment newInstance(String title, int index){
        UserinfoFragment ra= new UserinfoFragment();
        Bundle args = new Bundle();
        args.putString(ARG_TITLE,title);
        args.putInt(ARG_INDEX, index);
        ra.setArguments(args);
        return ra;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_userinfo, container, false);
    }

}
