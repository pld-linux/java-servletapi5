#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java
Summary:	Java servlet and JSP implementation classes
Summary(pl.UTF-8):	Klasy z implementacją Java Servlet i JSP
Name:		java-servletapi5
Version:	5.5.27
Release:	1
License:	Apache
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/tomcat/tomcat-5/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
# Source0-md5:	eb3f196013550b9b1684e4ff18593a8e
Patch0:		jakarta-servletapi5-target.patch
URL:		http://tomcat.apache.org/
BuildRequires:	ant
BuildRequires:	java-gcj-compat-devel
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Provides:	jakarta-servletapi5
Provides:	jsp
Provides:	servlet = %{version}
Provides:	servlet24
Provides:	servlet5
Provides:	servletapi5
Provides:	servletapi
Obsoletes:	jakarta-servletapi < 4
Obsoletes:	jakarta-servletapi5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This subproject contains the compiled code for the implementation
classes of the Java Servlet and JSP APIs (packages javax.servlet,
javax.servlet.http, javax.servlet.jsp, and javax.servlet.jsp.tagext).

%description -l pl.UTF-8
Ten podprojekt zawiera skompilowany kod implementacji klas API Java
Servlet i JSP (pakiety javax.servlet, javax.servlet.http,
javax.servlet.jsp i java.servlet.jsp.tagext).

%package javadoc
Summary:	servletapi documentation
Summary(pl.UTF-8):	Dokumentacja do servletapi
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
servletapi documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do servletapi.

%prep
%setup -qc
mv apache-tomcat-%{version}-src/servletapi/* .
%patch0 -p2

%build

%ant -f jsr154/build.xml dist \
	-Dbuild.compiler=gcj \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%ant -f jsr152/build.xml dist \
	-Dbuild.compiler=gcj \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%install
rm -rf $RPM_BUILD_ROOT

# JSP 2.0 and Servlet 2.4 classes
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a jsr152/dist/lib/jsp-api.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api-%{version}.jar
cp -a jsr154/dist/lib/servlet-api.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api-%{version}.jar
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api.jar
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servlet.jar
ln -s jsp-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api.jar

# not sure who expects what from which class
# servletapi4 contained both servlet-api and jsp-api classes in it's jar, so we link to api jar (or drop?)
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servletapi5.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a jsr152/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/jsp-api
cp -a jsr154/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/servlet-api
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
