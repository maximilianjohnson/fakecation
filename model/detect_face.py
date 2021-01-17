import cv2
import urllib.request as req
import sys
import numpy as np
import os
import matplotlib.pyplot as plt


#taken from learn opencv by Satya Mallick
def draw_delaunay(img, subdiv, delaunay_color ) :
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList :
        t = np.array(t).astype(np.int32)
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

       # if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
        cv2.line(img, pt1, pt2, delaunay_color, 1)
        cv2.line(img, pt2, pt3, delaunay_color, 1)
        cv2.line(img, pt3, pt1, delaunay_color, 1)

def show_images(img1, img2, title=""):
    f, axarr = plt.subplots(2,1)
    axarr[0].axis("off")
    axarr[1].axis("off")
    axarr[0].imshow(img1, cmap="gray")
    axarr[1].imshow(img2, cmap="gray")
    f.supertitle = title
    plt.show()

def overlay_face(rep_tri, tri, rep_img, img):
    dst = rep_img.copy()
    for face in rep_tri:
        rep = face
        triangles = tri
        for i in range(len(triangles)):
            t = np.array(rep[i]).astype(np.int32)
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])
            rect = np.array([pt1, pt2, pt3], dtype=np.int32)
            r = cv2.boundingRect(rect)

            t2 = np.array(triangles[i]).astype(np.int32)
            pt1 = (t2[0], t2[1])
            pt2 = (t2[2], t2[3])
            pt3 = (t2[4], t2[5])
            rect2 = np.array([pt1, pt2, pt3], dtype=np.int32)
            r2 = cv2.boundingRect(rect2)

            mask = np.zeros((r[3], r[2], 3), dtype = np.uint8)

            rect = np.float32(rect)
            rect2 = np.float32(rect2)

            for i in range(0, 3):
                rect[i] = [rect[i][0]-r[0], rect[i][1]-r[1]]
                rect2[i] = [rect2[i][0]-r2[0], rect2[i][1]-r2[1]]

            cv2.fillConvexPoly(mask, np.int32(rect), (1, 1, 1), 16, 0);
            #affine matrix
            M = cv2.getAffineTransform(rect2, rect)

            transform_img = img[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]

            #apply affine matrix to img
            dst = cv2.warpAffine(transform_img, M, (r[2], r[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)


            roi = rep_img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
            masked = cv2.bitwise_and(roi, cv2.bitwise_not(mask))
            #affine matrix
            rep_img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = rep_img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + dst * mask

    return rep_img;



def deep_fake(replace_url, face_path):
    img1 = "replace.jpg"
    img2 = "face.jpg"

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        resp = req.urlopen(replace_url)
        image = np.asarray(bytearray(resp.read()), dtype = np.uint8)
        face_replace_image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except Exception as e:
        print(e)
        face_replace_image = cv2.imread(cur_dir +  '/test2.jpeg')

    face_img = cv2.imread(face_path, cv2.IMREAD_COLOR)

    image_rgb = cv2.cvtColor(face_replace_image, cv2.COLOR_BGR2RGB)
    face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    # set dimension for cropping image
    x, y, width, depth = 50, 200, 950, 500

    rep_cropped = image_rgb[:len(image_rgb)-len(image_rgb)%3][:len(image_rgb[0])-len(image_rgb[0])%3]
    face_cropped = face_rgb[:len(face_rgb)-len(face_rgb)%3][:len(face_rgb[0])-len(face_rgb)%3]

    rep_final = rep_cropped.copy()
    rep_original = rep_cropped.copy()
    face_final = face_cropped.copy()

    # create a copy of the cropped image to be used later
    image_template = rep_cropped.copy()
    face_template = face_cropped.copy()

    # convert image to Grayscale
    image_gray = cv2.cvtColor(rep_cropped, cv2.COLOR_BGR2GRAY)
    face_gray = cv2.cvtColor(face_template, cv2.COLOR_BGR2GRAY)

    # remove axes and show image

    #show_images(image_gray, face_gray, "starting images")

    haarcascade = cur_dir + "/haarcascade_frontalface_alt2.xml"

    detector = cv2.CascadeClassifier(haarcascade)

    # Detect faces using the haarcascade classifier on the "grayscale image"
    faces_replace = detector.detectMultiScale(image_gray)
    faces = detector.detectMultiScale(face_gray)

    for face in faces:
    #     save the coordinates in x, y, w, d variables
        (x,y,w,d) = face
        # Draw a white coloured rectangle around each face using the face's coordinates
        # on the "image_template" with the thickness of 2
        cv2.rectangle(face_template, (x,y), (x+w, y+d), (255, 0, 0), 2)
    for face in faces_replace:
        (x,y,w,d) = face
        # Draw a white coloured rectangle around each face using the face's coordinates
        # on the "image_template" with the thickness of 2
        cv2.rectangle(image_template, (x,y), (x+w, y+d), (255, 0, 0), 2)



    #show_images(image_template, face_template, "faces")

    LBFmodel = cur_dir + "/lbfmodel.yaml"

    landmark_detector  = cv2.face.createFacemarkLBF()
    landmark_detector.loadModel(LBFmodel)

    # Detect landmarks on "image_gray"
    _, landmarks_replace = landmark_detector.fit(image_gray, faces_replace)
    _, landmarks = landmark_detector.fit(face_gray, faces)

    rep_hulls_img = rep_cropped.copy()
    hulls_img = face_cropped.copy()

    for landmark in landmarks:
        for (x,y) in landmark[0]:
            cv2.circle(hulls_img, (x,y), 1, (255, 0, 0))
    for landmark in landmarks_replace:
        for (x,y) in landmark[0]:
            cv2.circle(rep_hulls_img, (x,y), 1, (255, 0, 0))

    #show_images(rep_hulls_img, hulls_img)

    #get hulls from facial landmarks
    face_hulls = []
    for landmark in landmarks:
        hull = cv2.convexHull(landmark[0], returnPoints = False)
        hull = np.array(hull, dtype=np.int32).squeeze()
        face_hulls.append(hull)

    replace_hulls = []
    for landmark in landmarks_replace:
        hull = cv2.convexHull(landmark[0], returnPoints = False)
        hull = np.array(hull, dtype=np.int32).squeeze()
        replace_hulls.append(hull) 

    rep_tri_img = rep_cropped.copy()
    tri_img = face_cropped.copy()

    size = np.array(tri_img).shape
    rect = (0, 0, size[1], size[0])
    tri = cv2.Subdiv2D(rect)
    #TODO choose the face you want to upload but too hard for now
    face_hulls = face_hulls[0]

    #map triangle key to landmark index
    retrival = {}
    for i in face_hulls:
        (x,y) = (np.float32(landmarks[0][0][i]))
        retrival[(tri.insert((x,y)))] = i
    draw_delaunay(tri_img, tri, (255,0,0))

    triangles = tri.getTriangleList();

    rep_triangles = []
    for landmarks in landmarks_replace:
        cur_tri = []
        for t in triangles:
            (p1_x, p1_y, p2_x, p2_y, p3_x, p3_y) = t
            p1 = tri.findNearest((p1_x, p1_y))[0]
            p2 = tri.findNearest((p2_x, p2_y))[0]
            p3 = tri.findNearest((p3_x, p3_y))[0]
            coord = np.concatenate((landmarks[0][retrival[p1]], landmarks[0][retrival[p2]], landmarks[0][retrival[p3]]))
            cur_tri.append(coord)
        rep_triangles.append(cur_tri)

    final = overlay_face(rep_triangles, triangles, rep_final, face_final)


    size_x, size_y = len(final), len(final[0]);
    mask = np.zeros((size_x, size_y, 3), dtype = np.uint8)

    cv2.fillConvexPoly(mask, np.int32(landmarks_replace[0][0][face_hulls]), (255,255,255), 16, 0)

    points = landmarks_replace[0][0][replace_hulls[0]]

    M = cv2.moments(points)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    center = (cX, cY)

    mask_copy = mask.copy()

    cv2.circle(mask_copy, center, 1, (255,0,0))
    

    #show_images(final, mask_copy)
    output = cv2.seamlessClone(final, rep_original, mask, center, cv2.NORMAL_CLONE)

    final_file = cur_dir + '/../fakecation/static/assets/images/masked_img.jpg'  
    cv2.imwrite(final_file, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
    return final_file


if __name__ == '__main__':
    if(len(sys.argv) < 3 or len(sys.argv) > 3):
        deep_fake("","./me.png")
    else:
        deep_fake(sys.argv[1], sys.argv[2])
