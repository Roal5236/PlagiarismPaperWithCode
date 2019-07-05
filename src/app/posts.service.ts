import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class PostsService{
  private posts: object;
  private postUpdated = new Subject();
  private UploadFileText;
  private FileNameUpdated = new Subject();
  private selectedFile;
  private DisplaySpinnerObservable = new Subject();
  private displaySpinner;
  private OpenPanelObservable = new Subject();



  constructor(private http: HttpClient) { }

  getPostsUpdatedListner() {
    return this.postUpdated.asObservable();
  }

  fileUploadedListner(){
    return this.FileNameUpdated.asObservable();
  }

  displaySpinnerListner(){
    return this.DisplaySpinnerObservable.asObservable();
  }

  OpenPanelListner(){
    return this.OpenPanelObservable.asObservable();
  }

  getPostsFromServer(){
    this.http.get('http://127.0.0.1:5000/demo')
    .subscribe((postData) => {
      this.posts = postData;
      this.postUpdated.next(this.posts);
      console.log('this.posts-- ', this.posts);

      this.displaySpinner = 'none';
      this.DisplaySpinnerObservable.next(this.displaySpinner);
    });
  }


  OnUpload(event): void {
    console.log(event.target.files[0]);
    this.selectedFile = event.target.files[0];

    this.UploadFileText = event.target.files[0].name;
    this.FileNameUpdated.next(this.UploadFileText);

    this.displaySpinner = 'block';
    this.DisplaySpinnerObservable.next('block');

    const endpoint = 'http://127.0.0.1:5000/uploadFile';
    const formData: FormData = new FormData();
    formData.append('file', this.selectedFile);
    this.http.post(endpoint, formData).subscribe((res: any) => {
      console.log('Result -- ', res);
      this.FileNameUpdated.next('Uploaded');
      this.getPostsFromServer();
    });

  }

  send_post(txtz) {

    const sendBody = new URLSearchParams();
    sendBody.set('plag_text', txtz);

    this.displaySpinner = 'block';
    this.DisplaySpinnerObservable.next('block');

    const sendOptions = {
      headers: new HttpHeaders()
      .set('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')
      .set('Access-Control-Allow-Origin', '*')
    };
    this.http.post('http://127.0.0.1:5000/recieveText', sendBody.toString(), sendOptions).subscribe((res: any) => {
      console.log(res);
      this.getPostsFromServer();
    },
    err => {
      console.log('ERROR...', err);
    });
  }


  openPanel(i){
    this.OpenPanelObservable.next(i);
  }


}
