package ca.gcastle.bottomnavigation.view;

import android.animation.Animator;
import android.animation.AnimatorSet;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.content.Context;
import android.content.res.Configuration;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.os.Build;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.Display;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.widget.FrameLayout;

import java.util.ArrayList;
import java.util.List;

import ca.gcastle.bottomnavigation.R;
import ca.gcastle.bottomnavigation.listeners.OnChildClickedListener;

/**
 * The main View of this library.
 *
 * Created by graeme.castle on 12/04/2016.
 */
public class BottomNavigationView extends FrameLayout {

    // Used to intercept touch events in order to animate reveal effect
    private GestureDetector mDetector;

    // Used to paint reveal effect
    private Paint           mRadiusPaint;

    // Customisable Values
    private boolean mGrowTabs;
    private boolean mShowReveal;
    private int     mInitiallySelectedChild;
    private int     mTabGrowthModifier;
    private int     mExpandAnimationTime;

    // Helper value, contains width of unselected child views.
    private int mUnselectedChildSize;

    // Flag to indicate wether an animation is currently taking place.
    private boolean currentlyAnimating = false;

    // Changed by RadiusAnimationListener and read in onDraw for reveal effect
    private float radiusAnimationValue = 0;

    // Currently selected child
    private int currentlySelectedChild = 0;

    // Reveal centers (both current and next)
    private int cx;
    private int cy;

    // Next to select child and the touch centers for the reveal effect.
    private int itemToOpenAfterThisAnimation = -1;
    private int cxAfterThisAnimation = 0;
    private int cyAfterThisAnimation = 0;

    // Used to hold child widths, pushed to children in onLayout, changed
    private ArrayList<Integer> childWidths = new ArrayList<>();

    // Listener for when a child is clicked so that the client can handle them.
    private OnChildClickedListener onChildClickedListener;

    public BottomNavigationView(Context context, AttributeSet attrs) {
        super(context, attrs);

        mDetector = new GestureDetector(context, new GestureDetector.SimpleOnGestureListener() {
            @Override
            public boolean onSingleTapUp(MotionEvent e) {
                int widthPerChild = getWidth() / getChildCount();
                int childClicked = (int) (e.getX() / widthPerChild);

                if(onChildClickedListener != null) {
                    onChildClickedListener.onChildClicked(childClicked);
                }

                animateClick(childClicked, (int) e.getX(), (int) e.getY());

                return true;
            }
        });

        mRadiusPaint = new Paint();

        TypedArray a = getContext().obtainStyledAttributes(attrs, R.styleable.bottomNav);

        mGrowTabs               = a.getBoolean(R.styleable.bottomNav_navGrowTabs, true);
        mShowReveal             = a.getBoolean(R.styleable.bottomNav_navShowCircleReveal, true);
        mInitiallySelectedChild = a.getInt(R.styleable.bottomNav_navInitiallySelectedChild, 0);
        mTabGrowthModifier      = (int) a.getDimension(R.styleable.bottomNav_navGrowthModifier,
                                    BottomNavigationUtils.getPixelsFromDP(getContext(), 64));
        mExpandAnimationTime    = a.getInt(R.styleable.bottomNav_navInitiallySelectedChild, getResources().getInteger(android.R.integer.config_shortAnimTime));

        a.recycle();

        if(!mGrowTabs) {
            mTabGrowthModifier = 0;
        }
    }

    @Override
    protected void onFinishInflate() {
        super.onFinishInflate();

        if(getChildCount() <= 1) {
            throw new IllegalArgumentException(getClass().getSimpleName() +
                   " requires at least two children");
        }

        if(mInitiallySelectedChild >= getChildCount()) {
            throw new IllegalArgumentException(getClass().getSimpleName() +
                    " has too few children for an initial child index selection of " + mInitiallySelectedChild);
        }

        for (int i = 0; i < getChildCount(); i++) {
            if (!(getChildAt(i) instanceof BottomNavigationTabView)) {
                throw new ClassCastException(getClass().getSimpleName() +
                    " requires only " + BottomNavigationTabView.class.getSimpleName());
            }
        }

        setSelectedChild(mInitiallySelectedChild);
    }
//
//    @Override
//    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
//
//        int desiredWidth = 100;
//        int desiredHeight = 100;
//
//        int widthMode = MeasureSpec.getMode(widthMeasureSpec);
//        int widthSize = MeasureSpec.getSize(widthMeasureSpec);
//        int heightMode = MeasureSpec.getMode(heightMeasureSpec);
//        int heightSize = MeasureSpec.getSize(heightMeasureSpec);
//
//        int width;
//        int height;
//
//        //Measure Width
//        if (widthMode == MeasureSpec.EXACTLY) {
//            //Must be this size
//            width = widthSize;
//        } else if (widthMode == MeasureSpec.AT_MOST) {
//            //Can't be bigger than...
//            width = Math.min(desiredWidth, widthSize);
//        } else {
//            //Be whatever you want
//            width = desiredWidth;
//        }
//
//        //Measure Height
//        if (heightMode == MeasureSpec.EXACTLY) {
//            //Must be this size
//            height = heightSize;
//        } else if (heightMode == MeasureSpec.AT_MOST) {
//            //Can't be bigger than...
//            height = Math.min(desiredHeight, heightSize);
//        } else {
//            //Be whatever you want
//            height = desiredHeight;
//        }
//
//        //MUST CALL THIS
//        setMeasuredDimension(width, height);
//    }

    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        int width = r - l;
        int height = b - t;
        if(changed) {
            childWidths.clear();

            mUnselectedChildSize = (width - mTabGrowthModifier) / getChildCount();
            for(int i = 0; i < getChildCount(); i++) {
                if(i == mInitiallySelectedChild) {
                    childWidths.add(mUnselectedChildSize + mTabGrowthModifier);
                } else {
                    childWidths.add(mUnselectedChildSize);
                }
            }
        }
        int left = 0;
        for(int i = 0; i < getChildCount(); i++) {
            int childWidth = childWidths.get(i);
            getChildAt(i).layout(left, 0, left + childWidth, height);
            left += childWidth;
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        mDetector.onTouchEvent(event);
        return true;
    }

    public void setOnChildClickedListener(OnChildClickedListener listener) {
        this.onChildClickedListener = listener;
    }

    /*
     * Can be called to instantly select the current child. Must not be called mid-animation.
     */
    public void setSelectedChild(int selectedChildIndex) {
        BottomNavigationTabView selectedChild =
                (BottomNavigationTabView) getChildAt(selectedChildIndex);
        selectedChild.setSelected();
        setBackgroundColor(selectedChild.getColor());
    }

    /*
     * Can be used to start an animation (or queue an animation) from the center of the selected
     * child
     *
     * @param child     The index of the child you wish to animate to
     * @param activateChildOnClickListener boolean value to indicate whether the child tabs
     *                                     onClickListener should fire
     */
    public void animateToChild(int child, boolean activateChildOnClickListener) {
        if(child >= getChildCount()) {
            throw new IllegalArgumentException(
                    "Cannot animate to child index " + child + ". " + getClass().getSimpleName() +
                            " only has " + getChildCount() + " children");
        }

        if(activateChildOnClickListener) {
            ((BottomNavigationTabView) getChildAt(child)).onClick();
        }

        int widthPerChild = getWidth() / getChildCount();
        int x = widthPerChild * child + (widthPerChild / 2);
        int y = getHeight() / 2;

        animateClick(child, x, y);
    }

    private void animateClick(int child, int x, int y) {
        if(currentlyAnimating) {
            itemToOpenAfterThisAnimation = child;
            cxAfterThisAnimation = x;
            cyAfterThisAnimation = y;
        } else {
            if(child != currentlySelectedChild) {
                cx = x;
                cy = y;
                animateChildToSelected(child);
            }
        }
    }


    private void animateChildToSelected(final int child) {
        currentlyAnimating = true;
        mRadiusPaint.setColor(((BottomNavigationTabView)getChildAt(child)).getColor());

        ValueAnimator expandAnimator = null;

        if(mGrowTabs) {
            expandAnimator = ValueAnimator.ofInt(0, mTabGrowthModifier);
            expandAnimator.addUpdateListener(new ViewWidthAnimator(child, currentlySelectedChild));
        }

        Animator maximiseAnimators = ((BottomNavigationTabView) getChildAt(child))
                .getAnimatorSet(true);
        Animator minimiseAnimators = ((BottomNavigationTabView) getChildAt(currentlySelectedChild))
                .getAnimatorSet(false);

        ValueAnimator radiusAnimator = null;
        if(mShowReveal) {
            radiusAnimator = ValueAnimator.ofFloat(0, getWidth());
            radiusAnimator.addUpdateListener(new RadiusAnimationListener());
        } else {
            setBackgroundColor(((BottomNavigationTabView)getChildAt(child)).getColor());
        }

        List<Animator> animations = new ArrayList<>();

        if(expandAnimator != null) animations.add(expandAnimator);
        if(maximiseAnimators != null) animations.add(maximiseAnimators);
        if(minimiseAnimators != null) animations.add(minimiseAnimators);
        if(radiusAnimator != null) animations.add(radiusAnimator);

        if(animations.size() > 0) {
            AnimatorSet set = new AnimatorSet();
            set.addListener(new EndAnimationListener());
            set.setDuration(mExpandAnimationTime);
            set.playTogether(animations);
            set.start();
        }

        currentlySelectedChild = child;
    }

    private class RadiusAnimationListener implements ValueAnimator.AnimatorUpdateListener {
        @Override
        public void onAnimationUpdate(ValueAnimator animation) {
            radiusAnimationValue = (float) animation.getAnimatedValue();
        }
    }

    private class EndAnimationListener implements Animator.AnimatorListener {

        @Override
        public void onAnimationEnd(Animator animation) {
            radiusAnimationValue = 0;
            setBackgroundColor(mRadiusPaint.getColor());
            currentlyAnimating = false;
            if(itemToOpenAfterThisAnimation != -1) {
                cx = cxAfterThisAnimation;
                cy = cyAfterThisAnimation;

                animateChildToSelected(itemToOpenAfterThisAnimation);
                itemToOpenAfterThisAnimation = -1;
                cxAfterThisAnimation = 0;
                cyAfterThisAnimation = 0;
            }
        }

        @Override public void onAnimationStart(Animator animation) {}
        @Override public void onAnimationCancel(Animator animation) {}
        @Override public void onAnimationRepeat(Animator animation) {}
    }

    private class ViewWidthAnimator implements ValueAnimator.AnimatorUpdateListener {
        int childIndexToExpand;
        int childIndexToMinimise;
        public ViewWidthAnimator(int childIndexToExpand, int childIndexToMinimise) {
            this.childIndexToExpand = childIndexToExpand;
            this.childIndexToMinimise = childIndexToMinimise;
        }

        @Override
        public void onAnimationUpdate(ValueAnimator animation) {
            childWidths.set(childIndexToExpand,
                            mUnselectedChildSize + (Integer) animation.getAnimatedValue());
            childWidths.set(childIndexToMinimise,
                            mUnselectedChildSize +
                                    (mTabGrowthModifier - (Integer) animation.getAnimatedValue()));
            requestLayout();
        }
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        if(radiusAnimationValue > 0) {
            canvas.drawCircle(cx, cy, radiusAnimationValue, mRadiusPaint);
        }
    }

    protected boolean shouldFitSystemWindow() {
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            return isTranslucentStatusbarEnabled() && hasSoftKeys() && getNavigationBarHeight() > 0;
        } else {
            return false;
        }
    }

    protected boolean isTranslucentStatusbarEnabled() {
        int id = getResources().getIdentifier("config_enableTranslucentDecor", "bool", "android");
        if (id == 0) {
            return false;
        } else {
            return getResources().getBoolean(id);
        }
    }

    // http://stackoverflow.com/a/14871974/726954
    protected boolean hasSoftKeys(){
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1){
            Display d = ((Activity)getContext()).getWindowManager().getDefaultDisplay();

            DisplayMetrics realDisplayMetrics = new DisplayMetrics();
            d.getRealMetrics(realDisplayMetrics);

            int realHeight = realDisplayMetrics.heightPixels;
            int realWidth = realDisplayMetrics.widthPixels;

            DisplayMetrics displayMetrics = new DisplayMetrics();
            d.getMetrics(displayMetrics);

            int displayHeight = displayMetrics.heightPixels;
            int displayWidth = displayMetrics.widthPixels;

            return (realWidth - displayWidth) > 0 || (realHeight - displayHeight) > 0;
        }

        // for the sake of checking if we're using transparent navigation bar
        return false;
    }

    protected int getNavigationBarHeight() {
        int id;

        if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT) {
            id = getResources().getIdentifier("navigation_bar_height", "dimen", "android");
        } else {
            id = getResources().getIdentifier("navigation_bar_height_landscape", "dimen", "android");
        }

        if (id > 0) {
            return getResources().getDimensionPixelSize(id);
        }

        return 0;
    }
}
