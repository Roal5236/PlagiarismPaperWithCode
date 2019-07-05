import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DispPlagComponent } from './disp-plag.component';

describe('DispPlagComponent', () => {
  let component: DispPlagComponent;
  let fixture: ComponentFixture<DispPlagComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DispPlagComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DispPlagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
