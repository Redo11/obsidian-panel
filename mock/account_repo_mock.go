// Code generated by MockGen. DO NOT EDIT.
// Source: github.com/DemoHn/obsidian-panel/app/providers/account (interfaces: Repository)

// Package mock is a generated GoMock package.
package mock

import (
	account "github.com/DemoHn/obsidian-panel/app/providers/account"
	gomock "github.com/golang/mock/gomock"
	reflect "reflect"
)

// MockRepository is a mock of Repository interface
type MockRepository struct {
	ctrl     *gomock.Controller
	recorder *MockRepositoryMockRecorder
}

// MockRepositoryMockRecorder is the mock recorder for MockRepository
type MockRepositoryMockRecorder struct {
	mock *MockRepository
}

// NewMockRepository creates a new mock instance
func NewMockRepository(ctrl *gomock.Controller) *MockRepository {
	mock := &MockRepository{ctrl: ctrl}
	mock.recorder = &MockRepositoryMockRecorder{mock}
	return mock
}

// EXPECT returns an object that allows the caller to indicate expected use
func (m *MockRepository) EXPECT() *MockRepositoryMockRecorder {
	return m.recorder
}

// InsertAccountData mocks base method
func (m *MockRepository) InsertAccountData(arg0 string, arg1 []byte, arg2 string) (*account.Model, error) {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "InsertAccountData", arg0, arg1, arg2)
	ret0, _ := ret[0].(*account.Model)
	ret1, _ := ret[1].(error)
	return ret0, ret1
}

// InsertAccountData indicates an expected call of InsertAccountData
func (mr *MockRepositoryMockRecorder) InsertAccountData(arg0, arg1, arg2 interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "InsertAccountData", reflect.TypeOf((*MockRepository)(nil).InsertAccountData), arg0, arg1, arg2)
}

// ListAccountsData mocks base method
func (m *MockRepository) ListAccountsData(arg0, arg1 *int) ([]account.Model, error) {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "ListAccountsData", arg0, arg1)
	ret0, _ := ret[0].([]account.Model)
	ret1, _ := ret[1].(error)
	return ret0, ret1
}

// ListAccountsData indicates an expected call of ListAccountsData
func (mr *MockRepositoryMockRecorder) ListAccountsData(arg0, arg1 interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "ListAccountsData", reflect.TypeOf((*MockRepository)(nil).ListAccountsData), arg0, arg1)
}
