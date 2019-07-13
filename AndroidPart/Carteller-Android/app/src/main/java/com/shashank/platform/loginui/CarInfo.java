package com.shashank.platform.loginui;

import java.util.List;

public class CarInfo {

    /**
     * log_id : 8652631564818342637
     * vehicle_num : 1
     * vehicle_info : [{"attributes":{"direction":{"score":0.9457915425300598,"name":"左后方"},"copilot_belt":{"score":0.004232525825500488},"copilot_visor":{"score":0.1863059401512146},"rearview_item":{"score":0.01160651445388794},"driver_visor":{"score":0.1001607179641724},"in_car_item":{"score":0.6117159724235535},"skylight":{"score":0.8020655512809753},"copilot":{"score":0.1519237756729126},"window_rain_eyebrow":{"score":0.04997068643569946},"vehicle_type":{"score":0.9970288872718811,"name":"小汽车"},"roof_rack":{"score":9.590983390808105E-4},"driver_belt":{"score":0.9485464692115784}},"location":{"width":330,"top":4,"left":40,"height":270}}]
     */

    private long log_id;
    private int vehicle_num;
    private List<VehicleInfoBean> vehicle_info;

    public long getLog_id() {
        return log_id;
    }

    public void setLog_id(long log_id) {
        this.log_id = log_id;
    }

    public int getVehicle_num() {
        return vehicle_num;
    }

    public void setVehicle_num(int vehicle_num) {
        this.vehicle_num = vehicle_num;
    }

    public List<VehicleInfoBean> getVehicle_info() {
        return vehicle_info;
    }

    public void setVehicle_info(List<VehicleInfoBean> vehicle_info) {
        this.vehicle_info = vehicle_info;
    }

    public static class VehicleInfoBean {
        /**
         * attributes : {"direction":{"score":0.9457915425300598,"name":"左后方"},"copilot_belt":{"score":0.004232525825500488},"copilot_visor":{"score":0.1863059401512146},"rearview_item":{"score":0.01160651445388794},"driver_visor":{"score":0.1001607179641724},"in_car_item":{"score":0.6117159724235535},"skylight":{"score":0.8020655512809753},"copilot":{"score":0.1519237756729126},"window_rain_eyebrow":{"score":0.04997068643569946},"vehicle_type":{"score":0.9970288872718811,"name":"小汽车"},"roof_rack":{"score":9.590983390808105E-4},"driver_belt":{"score":0.9485464692115784}}
         * location : {"width":330,"top":4,"left":40,"height":270}
         */

        private AttributesBean attributes;
        private LocationBean location;

        public AttributesBean getAttributes() {
            return attributes;
        }

        public void setAttributes(AttributesBean attributes) {
            this.attributes = attributes;
        }

        public LocationBean getLocation() {
            return location;
        }

        public void setLocation(LocationBean location) {
            this.location = location;
        }

        public static class AttributesBean {
            /**
             * direction : {"score":0.9457915425300598,"name":"左后方"}
             * copilot_belt : {"score":0.004232525825500488}
             * copilot_visor : {"score":0.1863059401512146}
             * rearview_item : {"score":0.01160651445388794}
             * driver_visor : {"score":0.1001607179641724}
             * in_car_item : {"score":0.6117159724235535}
             * skylight : {"score":0.8020655512809753}
             * copilot : {"score":0.1519237756729126}
             * window_rain_eyebrow : {"score":0.04997068643569946}
             * vehicle_type : {"score":0.9970288872718811,"name":"小汽车"}
             * roof_rack : {"score":9.590983390808105E-4}
             * driver_belt : {"score":0.9485464692115784}
             */

            private DirectionBean direction;
            private CopilotBeltBean copilot_belt;
            private CopilotVisorBean copilot_visor;
            private RearviewItemBean rearview_item;
            private DriverVisorBean driver_visor;
            private InCarItemBean in_car_item;
            private SkylightBean skylight;
            private CopilotBean copilot;
            private WindowRainEyebrowBean window_rain_eyebrow;
            private VehicleTypeBean vehicle_type;
            private RoofRackBean roof_rack;
            private DriverBeltBean driver_belt;

            public DirectionBean getDirection() {
                return direction;
            }

            public void setDirection(DirectionBean direction) {
                this.direction = direction;
            }

            public CopilotBeltBean getCopilot_belt() {
                return copilot_belt;
            }

            public void setCopilot_belt(CopilotBeltBean copilot_belt) {
                this.copilot_belt = copilot_belt;
            }

            public CopilotVisorBean getCopilot_visor() {
                return copilot_visor;
            }

            public void setCopilot_visor(CopilotVisorBean copilot_visor) {
                this.copilot_visor = copilot_visor;
            }

            public RearviewItemBean getRearview_item() {
                return rearview_item;
            }

            public void setRearview_item(RearviewItemBean rearview_item) {
                this.rearview_item = rearview_item;
            }

            public DriverVisorBean getDriver_visor() {
                return driver_visor;
            }

            public void setDriver_visor(DriverVisorBean driver_visor) {
                this.driver_visor = driver_visor;
            }

            public InCarItemBean getIn_car_item() {
                return in_car_item;
            }

            public void setIn_car_item(InCarItemBean in_car_item) {
                this.in_car_item = in_car_item;
            }

            public SkylightBean getSkylight() {
                return skylight;
            }

            public void setSkylight(SkylightBean skylight) {
                this.skylight = skylight;
            }

            public CopilotBean getCopilot() {
                return copilot;
            }

            public void setCopilot(CopilotBean copilot) {
                this.copilot = copilot;
            }

            public WindowRainEyebrowBean getWindow_rain_eyebrow() {
                return window_rain_eyebrow;
            }

            public void setWindow_rain_eyebrow(WindowRainEyebrowBean window_rain_eyebrow) {
                this.window_rain_eyebrow = window_rain_eyebrow;
            }

            public VehicleTypeBean getVehicle_type() {
                return vehicle_type;
            }

            public void setVehicle_type(VehicleTypeBean vehicle_type) {
                this.vehicle_type = vehicle_type;
            }

            public RoofRackBean getRoof_rack() {
                return roof_rack;
            }

            public void setRoof_rack(RoofRackBean roof_rack) {
                this.roof_rack = roof_rack;
            }

            public DriverBeltBean getDriver_belt() {
                return driver_belt;
            }

            public void setDriver_belt(DriverBeltBean driver_belt) {
                this.driver_belt = driver_belt;
            }

            public static class DirectionBean {
                /**
                 * score : 0.9457915425300598
                 * name : 左后方
                 */

                private double score;
                private String name;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }

                public String getName() {
                    return name;
                }

                public void setName(String name) {
                    this.name = name;
                }
            }

            public static class CopilotBeltBean {
                /**
                 * score : 0.004232525825500488
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class CopilotVisorBean {
                /**
                 * score : 0.1863059401512146
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class RearviewItemBean {
                /**
                 * score : 0.01160651445388794
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class DriverVisorBean {
                /**
                 * score : 0.1001607179641724
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class InCarItemBean {
                /**
                 * score : 0.6117159724235535
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class SkylightBean {
                /**
                 * score : 0.8020655512809753
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class CopilotBean {
                /**
                 * score : 0.1519237756729126
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class WindowRainEyebrowBean {
                /**
                 * score : 0.04997068643569946
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class VehicleTypeBean {
                /**
                 * score : 0.9970288872718811
                 * name : 小汽车
                 */

                private double score;
                private String name;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }

                public String getName() {
                    return name;
                }

                public void setName(String name) {
                    this.name = name;
                }
            }

            public static class RoofRackBean {
                /**
                 * score : 9.590983390808105E-4
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }

            public static class DriverBeltBean {
                /**
                 * score : 0.9485464692115784
                 */

                private double score;

                public double getScore() {
                    return score;
                }

                public void setScore(double score) {
                    this.score = score;
                }
            }
        }

        public static class LocationBean {
            /**
             * width : 330
             * top : 4
             * left : 40
             * height : 270
             */

            private int width;
            private int top;
            private int left;
            private int height;

            public int getWidth() {
                return width;
            }

            public void setWidth(int width) {
                this.width = width;
            }

            public int getTop() {
                return top;
            }

            public void setTop(int top) {
                this.top = top;
            }

            public int getLeft() {
                return left;
            }

            public void setLeft(int left) {
                this.left = left;
            }

            public int getHeight() {
                return height;
            }

            public void setHeight(int height) {
                this.height = height;
            }
        }
    }
}
