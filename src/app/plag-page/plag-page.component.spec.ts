import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlagPageComponent } from './plag-page.component';

describe('PlagPageComponent', () => {
  let component: PlagPageComponent;
  let fixture: ComponentFixture<PlagPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PlagPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlagPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
